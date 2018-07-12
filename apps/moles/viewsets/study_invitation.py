from django.db.models import Q
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.accounts.models import DoctorToPatient, PatientConsent
from apps.accounts.models.participant import get_participant_patient
from apps.accounts.permissions import IsOnlyDoctor
from apps.accounts.permissions.is_partipicant import IsParticipant
from apps.accounts.serializers import PatientSerializer
from ..models import StudyInvitation, StudyInvitationStatus, StudyToPatient
from ..serializers import StudyInvitationBaseSerializer, \
    StudyInvitationSerializer, StudyInvitationForDoctorSerializer


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
    def approve(self, request, pk):
        invitation = self.get_object()

        doctor = invitation.doctor
        doctor_encryption_key = self.request.data['doctor_encryption_key']
        patient_consent = PatientConsent.objects.get(
            pk=self.request.data['consent_pk'])
        patient = get_participant_patient(self.request.user.doctor_role)
        if patient_consent.patient != patient:
            raise ValidationError(
                'Patient in consent does not match request patient')

        DoctorToPatient.objects.update_or_create(
            doctor=doctor,
            patient=patient,
            defaults={'encrypted_key': doctor_encryption_key})

        if doctor.my_coordinator and \
                'coordinator_encryption_key' in self.request.data:
            DoctorToPatient.objects.update_or_create(
                doctor=doctor.my_coordinator.doctor_ptr,
                patient=patient,
                defaults={
                    'encrypted_key':
                        self.request.data['coordinator_encryption_key']
                })

        StudyToPatient.objects.create(
            study=invitation.study,
            patient=patient,
            patient_consent=patient_consent)

        invitation.status = StudyInvitationStatus.ACCEPTED
        invitation.save(update_fields=['status'])
        return Response(StudyInvitationSerializer(
            context=self.get_serializer_context(),
            instance=invitation
        ).data)

    @detail_route(methods=['POST'])
    def decline(self, request, pk):
        invitation = self.get_object()
        invitation.status = StudyInvitationStatus.DECLINED
        invitation.save(update_fields=['status'])

        return Response(StudyInvitationSerializer(
            context=self.get_serializer_context(),
            instance=invitation
        ).data)


class StudyInvitationForDoctorViewSet(viewsets.GenericViewSet,
                                      mixins.ListModelMixin):
    queryset = StudyInvitation.objects.all()
    serializer_class = StudyInvitationForDoctorSerializer
    permission_classes = (IsOnlyDoctor,)

    def get_queryset(self):
        qs = super(StudyInvitationForDoctorViewSet, self).get_queryset()
        return qs.filter(
            doctor=self.request.user.doctor_role,
            patient__isnull=False
        ).filter(
            Q(status=StudyInvitationStatus.NEW) |
            Q(status=StudyInvitationStatus.DECLINED))

    def get_serializer_class(self):
        if self.action == 'create':
            return StudyInvitationBaseSerializer
        else:
            return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.doctor = self.request.user.doctor_role
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)

    # PatientSerializer with partial=True is used for creating
    # DoctorToPatient links. So need to post with `encryption_keys` param
    @detail_route(methods=['POST'])
    def approve(self, request, pk):
        invitation = self.get_object()
        patient_serializer = PatientSerializer(
            invitation.patient,
            data=request.data, context={'request': request}, partial=True)
        patient_serializer.is_valid(raise_exception=True)
        patient_serializer.save()

        invitation.status = StudyInvitationStatus.ACCEPTED
        invitation.save(update_fields=['status'])

        serializer = self.get_serializer(instance=invitation)
        return Response(serializer.data)

    @detail_route(methods=['POST'])
    def decline(self, request, pk):
        invitation = self.get_object()
        invitation.status = StudyInvitationStatus.DECLINED
        invitation.save(update_fields=['status'])

        serializer = self.get_serializer(instance=invitation)
        return Response(serializer.data)
