from django.contrib import admin


class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',)
    search_fields = ('first_name', 'last_name')
    add_fieldsets = ((None, {
        'classes': ('wide',),
        'fields': (
            'doctor', 'mrn', 'first_name', 'last_name', 'date_of_birth',
            'sex', 'race', 'address',)
    }),)


    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(PatientAdmin, self).get_fieldsets(request, obj)
