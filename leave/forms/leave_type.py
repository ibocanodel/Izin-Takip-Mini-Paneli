from django import forms

from leave.models import LeaveType


class LeaveTypeForm(forms.ModelForm):
    class Meta:
        model = LeaveType
        fields = ["name", "annual_leave_days", "count_on_total_days"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        days = self.cleaned_data.get("annual_leave_days")
        if days is None and days <= 0:
            raise forms.ValidationError("İzin günü sayısı 0'dan büyük olmalıdır.")
        qs = LeaveType.objects.filter(name__iexact=name, is_deleted=False)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("Bu isimde bir leave_type zaten var.")
        return name
