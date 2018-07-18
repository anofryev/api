from django import forms
from django.contrib import admin

from ..models import ConsentDoc


class ConsentDocAdminForm(forms.ModelForm):
    def save(self, commit=True):
        self.instance.is_default_consent = True
        return super(ConsentDocAdminForm, self).save(commit)

    class Meta:
        model = ConsentDoc
        fields = '__all__'


class ConsentDocAdmin(admin.ModelAdmin):
    model = ConsentDoc
    form = ConsentDocAdminForm

    fieldsets = (
        (None, {'fields': ('file', 'original_filename',)}),
    )

    def get_queryset(self, request):
        queryset = super(ConsentDocAdmin, self).get_queryset(request)
        return queryset.filter(is_default_consent=True)
