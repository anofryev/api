from django.contrib import admin

from .doctor import DoctorAdmin
from .coordinator import CoordinatorAdmin
from .patient import PatientAdmin
from .patient_consent import PatientConsentAdmin
from ..models import Patient, PatientConsent, Doctor, Coordinator, Site


admin.site.register(Patient, PatientAdmin)
admin.site.register(PatientConsent, PatientConsentAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Coordinator, CoordinatorAdmin)
admin.site.register(Site)
