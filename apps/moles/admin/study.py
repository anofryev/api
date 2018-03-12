from django import forms
from django.contrib import admin

from ..models import Study, StudyToPatient
from apps.accounts.models import Patient


class StudyAdminForm(forms.ModelForm):
    patients = forms.ModelMultipleChoiceField(
        queryset=Patient.objects.all(),
        required=False
    )

    def _save_m2m(self):
        cleaned_data = self.cleaned_data
        for patient in cleaned_data['patients']:
            StudyToPatient.objects.create(
                study=self.instance,
                patient=patient
            )

    class Meta:
        model = Study
        fields = '__all__'


class StudyAdmin(admin.ModelAdmin):
    form = StudyAdminForm
    model = Study
