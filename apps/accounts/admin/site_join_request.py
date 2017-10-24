from django.contrib.admin import ModelAdmin
from fsm_admin.mixins import FSMTransitionMixin


class SiteJoinRequestAdmin(FSMTransitionMixin, ModelAdmin):
    fsm_field = ['state', ]
