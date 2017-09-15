from django import forms
from django.contrib import admin
from ..models import Doctor, Coordinator


class CoordinatorForm(forms.ModelForm):
    doctor_ptr = forms.ModelChoiceField(
        queryset=Doctor.objects.none(), required=True)

    def __init__(self, *args, **kwargs):
        super(CoordinatorForm, self).__init__(*args, **kwargs)
        self.fields['doctor_ptr'].queryset = Doctor.objects.exclude(
            id__in=Coordinator.objects.values_list(
                'doctor_ptr', flat=True))

    class Meta:
        model = Coordinator
        fields = ('doctor_ptr', )


class CoordinatorAdmin(admin.ModelAdmin):
    list_display = ('name', )

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return ('doctor_ptr', )
        return []

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs['form'] = CoordinatorForm
        return super(CoordinatorAdmin, self).get_form(request, obj, **kwargs)

    def get_queryset(self, *args, **kwargs):
        return super(CoordinatorAdmin, self).get_queryset(
            *args, **kwargs).select_related('doctor_ptr')

    def name(self, obj):
        return obj.doctor_ptr.__str__()
