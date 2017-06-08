from rest_framework import generics, response, status

from ..serializers import DoctorSerializer
from ..permissions import IsDoctor


class CurrentUserView(generics.GenericAPIView):
    permission_classes = (IsDoctor, )

    def get_serializer_class(self):
        user = self.request.user

        if hasattr(user, 'doctor_role'):
            return DoctorSerializer

        raise NotImplementedError

    def get_object(self):
        user = self.request.user

        if hasattr(user, 'doctor_role'):
            return user.doctor_role

        raise NotImplementedError

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance)
        return response.Response(
            data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(
            data=serializer.data, status=status.HTTP_200_OK)


current_user_view = CurrentUserView.as_view()
