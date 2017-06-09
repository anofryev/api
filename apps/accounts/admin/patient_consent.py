from django.contrib import admin


class PatientConsentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'date_created', 'date_expired', )
    fieldsets = (
        (None, {'fields': ('patient', 'date_expired', 'signature', )}),
    )
    readonly_fields = ('date_expired', )
