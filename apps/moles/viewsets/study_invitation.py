from rest_framework import viewsets, mixins
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ValidationError

from apps.accounts.models import DoctorToPatient
from apps.accounts.permissions.is_partipicant import IsParticipant
from ..models import StudyInvitation, StudyInvitationStatus
from ..serializers import StudyInvitationSerializer


class StudyInvitationViewSet(viewsets.GenericViewSet,
                             mixins.ListModelMixin):
    queryset = StudyInvitation.objects.all()
    serializer_class = StudyInvitationSerializer
    permission_classes = (IsParticipant,)

    def get_queryset(self):
        qs = super(StudyInvitationViewSet, self).get_queryset()
        return qs.filter(
            email=self.request.user.doctor_role__email,
            status=StudyInvitationStatus.NEW)

    @detail_route(methods=['POST'])
    def approve(self):
        invitation = self.get_object()
        invitation.status = StudyInvitationStatus.ACCEPTED
        invitation.save(update_fields=['status'])

        encryption_keys = self.request.data['encryption_keys']
        doctor = invitation.doctor
        if doctor.pk not in encryption_keys:
            raise ValidationError(
                'You doesn\'t not pass encryption key of doctor')

        patient = DoctorToPatient.objects.get(
            doctor=self.request.user.doctor_role
        ).patient

        DoctorToPatient.objects.update_or_create(
            doctor=doctor,
            patient=patient,
            defaults={'encrypted_key': encryption_keys[doctor.pk]})

        return StudyInvitationSerializer(instance=invitation).data

    @detail_route(methods=['POST'])
    def decline(self):
        invitation = self.get_object()
        invitation.status = StudyInvitationStatus.DECLINED
        invitation.save(update_fields=['status'])

        return StudyInvitationSerializer(instance=invitation).data
