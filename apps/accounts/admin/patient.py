from django.contrib import admin


class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',)
    search_fields = ('first_name', 'last_name')
    fieldsets = (
        ('Personal info', {'fields': (
            'doctor', 'first_name', 'last_name', 'date_of_birth', 'photo',
            'sex', 'race', 'address')}),
    )
