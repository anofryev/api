from django.contrib import admin

from .anatomical_site import AnatomicalSiteAdmin
from .patient_anatomical_site import PatientAnatomicalSiteAdmin
from .mole import MoleAdmin
from ..models import AnatomicalSite, PatientAnatomicalSite, Mole


admin.site.register(AnatomicalSite, AnatomicalSiteAdmin)
admin.site.register(PatientAnatomicalSite, PatientAnatomicalSiteAdmin)
admin.site.register(Mole, MoleAdmin)
