from rest_framework import viewsets, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import list_route

from apps.accounts.serializers import DoctorSerializer
from apps.moles.models import StudyInvitation
from ..serializers import DoctorWithSitesSerializer, DoctorKeySerializer
from ..models import Doctor
from ..permissions import IsCoordinator, IsDoctor


class DoctorViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    serializer_class = DoctorWithSitesSerializer
    queryset = Doctor.objects.filter(
        participant_role__isnull=True
    )
    permission_classes = (IsCoordinator, )

    def get_queryset(self):
        return super(DoctorViewSet, self)\
            .get_queryset()\
            .annotate_sites()

    @list_route(methods=['GET'], permission_classes=(IsDoctor,))
    def public_keys(self, request, *args, **kwargs):
        doctor_pks = request.GET.get('doctors').split(',')
        return Response(DoctorKeySerializer(
            Doctor.objects.filter(pk__in=doctor_pks),
            many=True
        ).data)

    @list_route(methods=['GET'], permission_classes=(IsDoctor,))
    def get_by_email(self, request, *args, **kwargs):
        email = request.GET.get('email')
        if StudyInvitation.objects.filter(
                email=email,
                patient__isnull=False).exists():
            raise ValidationError('email_used_by_the_patient')
        doctor = Doctor.objects.filter(email=email).first()
        return Response(DoctorSerializer(doctor).data if doctor else {})
