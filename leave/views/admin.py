from django.contrib import messages
from django.shortcuts import redirect, render

from leave.forms.admin import AppSettingsForm
from leave.models import AppSettings


def update_settings(request):
    settings, _ = AppSettings.objects.get_or_create(pk=1) 

    if request.method == "POST":
        form = AppSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Ayarlar güncellendi.")
            return redirect("update_settings")
    else:
        form = AppSettingsForm(instance=settings)

    return render(request, "update_settings.html", {"form": form})