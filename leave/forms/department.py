from django import forms

from leave.models import Department


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        qs = Department.objects.filter(name__iexact=name, is_deleted=False)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("Bu isimde bir departman zaten var.")
        return name
