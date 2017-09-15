from django.contrib import admin


class PatientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'sex', 'race', )
    readonly_fields = ('first_name', 'last_name', 'date_of_birth', 'mrn', )
    fieldsets = (
        ('Public info', {'fields': (
            'photo', 'sex', 'race', )}),
        ('Encrypted data', {'fields': (
            'first_name', 'last_name', 'date_of_birth', 'mrn', )})
    )
