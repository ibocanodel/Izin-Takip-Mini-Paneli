from django import forms

from leave.models import AppSettings


class AppSettingsForm(forms.ModelForm):
    class Meta:
        model = AppSettings
        fields = [
            "default_password",
            "annual_leave_days",
            "work_days",
            "allow_request_past_leaves",
            "allow_exceed_total_leave_days",
        ]
