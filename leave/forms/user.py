from django import forms
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from leave.models import Employee


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


class ProfileUpdateForm(forms.ModelForm):
    new_password = forms.CharField(
        required=False, widget=forms.PasswordInput, label="Yeni Şifre"
    )
    confirm_password = forms.CharField(
        required=False, widget=forms.PasswordInput, label="Şifre Tekrar"
    )

    class Meta:
        model = Employee
        fields = ["name"]

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password or confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError("Şifreler eşleşmiyor.")

            if len(new_password) < 8:
                raise forms.ValidationError("Şifre en az 8 karakter olmalıdır.")
            if not any(c.isalpha() for c in new_password):
                raise forms.ValidationError("Şifre en az bir harf içermelidir.")
            if not any(c.isdigit() for c in new_password):
                raise forms.ValidationError("Şifre en az bir rakam içermelidir.")

            cleaned_data["password"] = make_password(new_password)

        return cleaned_data


class CreateEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["name", "email", "department", "work_start_date", "role"]
        widgets = {
            "work_start_date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Geçerli bir e-posta adresi girin.")
        return email


class UpdateEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["name", "email", "department", "role", "work_start_date"]
        widgets = {
            "work_start_date": forms.DateInput(
                attrs={"type": "date"}, format="%Y-%m-%d"
            )
        }
