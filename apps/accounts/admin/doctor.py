from django.contrib.auth.admin import UserAdmin


class DoctorAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name',
                    'is_active', 'approved_by_coordinator', )
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
        ('Active status', {
            'fields': ('is_active', 'approved_by_coordinator', )
        }),
        ('Admin settings', {
            'fields': ('is_staff', 'is_superuser',
                       'groups', 'user_permissions'),
            'classes': ('collapse', ),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super(DoctorAdmin, self).get_form(request, obj, **kwargs)
        qs = form.base_fields['my_coordinator'].queryset
        form.base_fields['my_coordinator'].queryset = qs.select_related(
            'doctor_ptr')
        form.base_fields['my_coordinator'].label_from_instance = \
            lambda obj: obj.doctor_ptr.__str__()
        return form
