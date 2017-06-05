from django.contrib import admin

from .doctor import DoctorAdmin
from .patient import PatientAdmin
from ..models import User, Patient, Doctor


admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)
