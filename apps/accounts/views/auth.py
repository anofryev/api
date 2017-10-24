from djoser.views import PasswordResetConfirmView


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    def _action(self, serializer):
        result = super(MyPasswordResetConfirmView, self)._action(serializer)
        doctor = serializer.user.doctor_role
        doctor.private_key = ''
        doctor.save(update_fields=['private_key'])
        return result


reset_confirmation_view = MyPasswordResetConfirmView.as_view()
