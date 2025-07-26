from datetime import date, timedelta

from dateutil.relativedelta import relativedelta
from django import forms

from leave.models import AppSettings, Employee, Leave, LeaveType


class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ["leave_type", "start_date", "end_date", "business_days"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        self.employee: Employee = kwargs.pop("employee", None)
        self.force_submit = kwargs.pop("force_submit", False)
        super().__init__(*args, **kwargs)

    def get_leave_period_year(self, date):
        """
        Returns the leave year period (e.g. 2025-2026) based on employee's work_start_date.
        """
        work_start = self.employee.work_start_date
        current = work_start
        year = 0

        while True:
            period_start = work_start + relativedelta(years=year)
            period_end = work_start + relativedelta(years=year + 1) - timedelta(days=1)
            if period_start <= date <= period_end:
                return year, period_start, period_end
            year += 1

    def calculate_business_days(self, start_date: date, end_date: date, work_days):
        days = 0
        current = start_date
        while current <= end_date:
            if current.weekday() in work_days:
                days += 1
            current += timedelta(days=1)
        return days

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        leave_type = cleaned_data.get("leave_type")

        settings = AppSettings.objects.first()
        if settings is None:
            return
        allow_past = settings.allow_request_past_leaves if settings else False
        working_days = [1, 2, 3, 4, 5]

        if settings and settings.work_days:
            working_days = list(map(int, settings.work_days.split(",")))
        today = date.today()
        if not allow_past:
            if start_date and start_date < today:
                self.add_error("start_date", "Başlangıç tarihi bugünden önce olamaz.")

            if end_date and end_date < today:
                self.add_error("end_date", "Bitiş tarihi bugünden önce olamaz.")

        if start_date and end_date and start_date > end_date:
            self.add_error(
                "start_date", "Bitiş tarihi, başlangıç tarihinden önce olamaz."
            )

        if (start_date and start_date < self.employee.work_start_date) or (
            end_date and end_date < self.employee.work_start_date
        ):
            self.add_error(
                "start_date", "İzin tarihi işe başlangıç tarihinden önce olamaz"
            )

        current_request_business_days = self.calculate_business_days(
            start_date, end_date, working_days
        )
        if self.employee and start_date and end_date:
            overlap_exists = Leave.objects.filter(
                employee=self.employee,
                is_deleted=False,
                start_date__lte=end_date,
                end_date__gte=start_date,
            ).exists()

            if overlap_exists:
                self.add_error(
                    "start_date",
                    "Bu tarihler arasında başka bir izin talebiniz bulunmaktadır.",
                )
            start_period, period_start, period_end = self.get_leave_period_year(
                start_date
            )
            end_period, _, _ = self.get_leave_period_year(end_date)
            if start_period != end_period:
                self.add_error(
                    "start_date",
                    "Başlangıç ve bitiş tarihleri aynı izin döneminde olmalıdır.",
                )

            leaves = Leave.objects.filter(
                employee=self.employee,
                start_date__lte=period_end,
                end_date__gte=period_start,
            )

            leave_type = LeaveType.objects.get(id=leave_type.id)

            leaves_in_current_leave_type = leaves.filter(leave_type=leave_type)
            leave_type_count = 0
            for leave in leaves_in_current_leave_type:
                leave_type_count += self.calculate_business_days(
                    leave.start_date, leave.end_date, working_days
                )
            if (
                leave_type_count + current_request_business_days
                > leave_type.annual_leave_days
            ):
                if settings.allow_exceed_total_leave_days and not self.force_submit:
                    self.add_error(
                        None,
                        "Bu izin türündeki toplam limiti aştınız.Devam etmek istiyor musunuz?",
                    )
                elif not settings.allow_exceed_total_leave_days:
                    self.add_error(
                        "start_date", "Bu izin türündeki toplam limiti aştınız"
                    )

            if leave_type.count_on_total_days:
                all_leaves = leaves.filter(leave_type__count_on_total_days=True)
                all_leave_count = 0
                for leave in all_leaves:
                    all_leave_count += self.calculate_business_days(
                        leave.start_date, leave.end_date, working_days
                    )
                if (
                    all_leave_count + current_request_business_days
                    > settings.annual_leave_days
                ):
                    if settings.allow_exceed_total_leave_days and not self.force_submit:
                        self.add_error(
                            None,
                            "Toplam izin limiti aştınız.Devam etmek istiyor musunuz?",
                        )
                    elif not settings.allow_exceed_total_leave_days:
                        self.add_error("start_date", "Toplam izin limiti aştınız")

        return cleaned_data
