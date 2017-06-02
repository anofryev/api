from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sites.shortcuts import get_current_site


class UserPasswordResetView(GenericAPIView):

    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):

        if 'email' not in request.data:
            return Response({
                    'Error': 'This api endpoint needs an "email" attribute.'
                },
                status=status.HTTP_400_BAD_REQUEST)

        reset_form = PasswordResetForm(request.data)

        if reset_form.is_valid():
            reset_form.save(
                domain_override=get_current_site(request),
                from_email='test@example.com')

        response = {'success': 'Reset email sent'}

        return Response(response, status=status.HTTP_200_OK)


user_password_reset_view = UserPasswordResetView.as_view()
