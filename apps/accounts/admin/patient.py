from django.contrib import admin


class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',)
    search_fields = ('first_name', 'last_name')
    fieldsets = ((None, {
        'classes': ('wide',),
        'fields': (
            'doctor', 'mrn', 'first_name', 'last_name', 'photo',
            'date_of_birth', 'sex', 'race', 'address',)
    }),)
