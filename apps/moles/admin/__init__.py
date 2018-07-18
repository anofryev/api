from django.contrib import admin

from .anatomical_site import AnatomicalSiteAdmin
from .patient_anatomical_site import PatientAnatomicalSiteAdmin
from .mole import MoleAdmin
from .study import StudyAdmin
from .consent_docs import ConsentDocAdmin
from ..models import AnatomicalSite, PatientAnatomicalSite, Mole, Study, \
    StudyToPatient, StudyInvitation, ConsentDoc


admin.site.register(AnatomicalSite, AnatomicalSiteAdmin)
admin.site.register(PatientAnatomicalSite, PatientAnatomicalSiteAdmin)
admin.site.register(Mole, MoleAdmin)
admin.site.register(Study, StudyAdmin)
admin.site.register(StudyToPatient)
admin.site.register(StudyInvitation)
admin.site.register(ConsentDoc, ConsentDocAdmin)
