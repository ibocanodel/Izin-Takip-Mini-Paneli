from django.contrib.auth.hashers import check_password, make_password
from django.db import models

from leave.constants import Role_DB


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ActiveManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True


class Department(BaseModel):
    name = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class LeaveType(BaseModel):
    name = models.CharField(max_length=100)
    annual_leave_days = models.IntegerField(default=0)
    count_on_total_days = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Employee(BaseModel):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.IntegerField(choices=Role_DB.choices, default=Role_DB.NORMAL_EMPLOYEE)
    work_start_date = models.DateField(null=False)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class Leave(BaseModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    business_days = models.PositiveIntegerField()


class AppSettings(BaseModel):
    default_password = models.CharField(max_length=100, default="test1234")
    annual_leave_days = models.PositiveIntegerField(default=14)
    work_days = models.CharField(
        max_length=20,
        default="1,2,3,4,5",  # Pazartesi=1 ... Pazar=7
        help_text="Çalışma günlerini virgülle ayır (1=Ptsi, ..., 7=Pazar)",
    )
    allow_request_past_leaves = models.BooleanField(default=False)
    allow_exceed_total_leave_days = models.BooleanField(default=True)
