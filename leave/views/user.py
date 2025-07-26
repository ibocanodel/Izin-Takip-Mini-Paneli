from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect, render

from leave.forms.user import LoginForm, ProfileUpdateForm
from leave.models import Employee


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                employee = Employee.objects.get(email=form.cleaned_data['email'])
                if employee.check_password(form.cleaned_data['password']):
                    request.session['employee_id'] = employee.id
                    return redirect('leave_list')
                else:
                    messages.error(request, "Şifre hatalı.")
            except Employee.DoesNotExist:
                messages.error(request, "Kullanıcı bulunamadı.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')



def my_profile(request):
    employee_id = request.session.get("employee_id")
    employee = Employee.objects.get(id=employee_id)

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=employee)
        if form.is_valid():

            if form.cleaned_data.get("password"):
                employee.password = form.cleaned_data["password"]
            employee.name = form.cleaned_data["name"]
            employee.save()
            messages.success(request, "Profil başarıyla güncellendi.")
            return redirect("/")
    else:
        form = ProfileUpdateForm(instance=employee)

    return render(request, "my_profile.html", {
        "form": form,
        "employee": employee,
    })