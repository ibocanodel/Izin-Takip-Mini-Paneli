from enum import IntEnum

from django.db import models


class Role(IntEnum):
    NORMAL_EMPLOYEE = 1
    ADMIN = 2
    SUPER_ADMIN = 3


class Role_DB(models.IntegerChoices):
    NORMAL_EMPLOYEE = (1,)
    ADMIN = (2,)
    SUPER_ADMIN = (3,)
