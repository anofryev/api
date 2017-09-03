from django.contrib.auth.admin import UserAdmin


class DoctorAdmin(UserAdmin):
    list_display = ('first_name', 'last_name',)
    search_fields = ('first_name', 'last_name')
    add_fieldsets = ((None, {
        'classes': ('wide',),
        'fields': (
            'email', 'first_name', 'last_name',
            'password1', 'password2',
            'my_coordinator', )
    }),)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name',
                                      'photo', 'department', 'degree',)}),
        ('Settings', {'fields': ('units_of_length', 'my_coordinator',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_active', )}),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super(DoctorAdmin, self).get_form(request, obj, **kwargs)
        qs = form.base_fields['my_coordinator'].queryset
        form.base_fields['my_coordinator'].queryset = qs.select_related(
            'doctor_ptr')
        form.base_fields['my_coordinator'].label_from_instance = \
            lambda obj: obj.doctor_ptr.__str__()
        return form
