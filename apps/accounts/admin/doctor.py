from django.contrib.auth.admin import UserAdmin


class DoctorAdmin(UserAdmin):
    list_display = ('first_name', 'last_name',)
    search_fields = ('first_name', 'last_name')
    add_fieldsets = ((None, {
        'classes': ('wide',),
        'fields': (
            'email', 'first_name', 'last_name', 'password1', 'password2',)
    }),)
