from django.contrib import admin


class PatientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'sex', 'race', )
    fieldsets = (
        ('Public info', {'fields': (
            'photo', 'sex', 'race', )}),
    )
