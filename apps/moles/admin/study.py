from django import forms
from django.contrib import admin

from ..models import Study
from apps.accounts.models import Patient


class StudyAdminForm(forms.ModelForm):
    patients = forms.ModelMultipleChoiceField(
        queryset=Patient.objects.all(),
        required=False
    )

    class Meta:
        model = Study
        fields = '__all__'


class StudyAdmin(admin.ModelAdmin):
    form = StudyAdminForm
    model = Study
