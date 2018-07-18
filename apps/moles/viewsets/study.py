from rest_framework import viewsets, mixins, status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from apps.accounts.models.coordinator import is_coordinator
from apps.accounts.models import Doctor, Patient
from apps.accounts.models.participant import is_participant, \
    get_participant_patient
from apps.accounts.serializers import PatientConsentSerializer
from apps.moles.models import StudyToPatient
from apps.moles.models.moles_mailer import AddParticipantNotification
from apps.moles.serializers.study import AddDoctorSerializer
from apps.accounts.permissions import IsCoordinator, IsDoctor
from apps.accounts.permissions.is_coordinator_of_doctor import \
    IsCoordinatorOfDoctor
from apps.accounts.viewsets.mixins import PatientInfoMixin
from apps.main.models import FlatBlock
from ..models import ConsentDoc, Study, StudyInvitation
from ..serializers import (
    ConsentDocSerializer, StudyBaseSerializer, StudyListSerializer,
    StudyInvitationSerializer)


class ConsentDocViewSet(viewsets.GenericViewSet,
                        mixins.CreateModelMixin):
    queryset = ConsentDoc.objects.all()
    serializer_class = ConsentDocSerializer
    permission_classes = (IsCoordinator,)

    @list_route(methods=['GET'], permission_classes=(IsDoctor,))
    def default(self, request):
        page = FlatBlock.objects.filter(slug='default_consent_form').first()
        return Response({
            'page': page.content if page else '',
            'docs': ConsentDocSerializer(
                ConsentDoc.objects.filter(is_default_consent=True),
                many=True).data
        })


class StudyViewSet(viewsets.GenericViewSet, PatientInfoMixin,
                   mixins.CreateModelMixin, mixins.UpdateModelMixin,
                   mixins.ListModelMixin, mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin):
    queryset = Study.objects.all().order_by('-pk')
    serializer_class = StudyListSerializer
    permission_classes = (IsDoctor,)

    def get_queryset(self):
        user = self.request.user.doctor_role
        if is_coordinator(user):
            return self.queryset.filter(author__doctor_ptr=user)
        elif is_participant(user):
            patient = get_participant_patient(user)
            if patient:
                return self.queryset.filter(patients__pk=patient.pk)
            else:
                return self.queryset.none()
        else:
            return self.queryset.filter(doctors__pk=user.pk)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return StudyBaseSerializer
        else:
            return self.serializer_class

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsCoordinator()]
        elif self.action == 'add_doctor':
            return [IsCoordinatorOfDoctor()]
        else:
            return super(StudyViewSet, self).get_permissions()

    # We redefine create, because need to use BaseSerializer on input and
    # ListSerializer on output
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        instance.author = request.user.doctor_role.coordinator_role
        instance.save(update_fields=['author'])

        headers = self.get_success_headers(serializer.data)
        return Response(
            StudyListSerializer(instance, context={'request': request}).data,
            status=status.HTTP_201_CREATED, headers=headers)

    @detail_route(methods=['GET'])
    def invites(self, request, pk):
        study = self.get_object()
        instance = study.studyinvitation_set.all()
        return Response(
            StudyInvitationSerializer(instance, context={'request': request},
                                      many=True).data
        )

    @detail_route(methods=['POST'])
    def add_doctor(self, request, pk):
        study = self.get_object()
        serializer = AddDoctorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        doctor_pk = serializer.data['doctor_pk']
        email_list = serializer.data['emails']
        fail_emails = {}

        study.doctors.add(doctor_pk)
        for email in email_list:
            check_doctor = Doctor.objects.filter(email=email).first()
            if check_doctor and not is_participant(check_doctor):
                fail_emails.update({
                    email: 'user is already doctor or coordinator'
                })
            else:
                if StudyInvitation.objects.filter(
                        email=email, study=study).exists():
                    fail_emails.update({
                        email: 'user is already participating'
                    })
                else:
                    StudyInvitation.objects.create(
                        email=email,
                        study=study,
                        doctor_id=doctor_pk)
                    AddParticipantNotification(
                        context={'study_id': study.pk,
                                 'study_title': study.title}).send([email])

        return Response({
            'all_success': len(fail_emails) == 0,
            'fail_emails': fail_emails
        })

    @detail_route(methods=['POST'])
    def add_consent(self, request, pk):
        """
        :param request: {patient_pk: X, signature: XX}
        :param pk:
        :return: Serialized study
        """
        study = self.get_object()
        patient = Patient.objects.get(pk=request.data.get('patient_pk'))

        serializer = PatientConsentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        consent = serializer.save(patient=patient)

        study_to_patient = StudyToPatient.objects.filter(
            study=study,
            patient=patient
        ).first()
        study_to_patient.patient_consent = consent
        study_to_patient.save()

        return Response(
            StudyListSerializer(study, context={'request': request}).data)
