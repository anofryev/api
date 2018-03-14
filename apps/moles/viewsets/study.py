from rest_framework import viewsets, mixins
from rest_framework.decorators import detail_route
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.accounts.models import Doctor
from apps.accounts.models.participant import is_participant
from apps.accounts.permissions import IsCoordinator, IsDoctor
from apps.accounts.permissions.is_coordinator_of_doctor import \
    IsCoordinatorOfDoctor
from apps.accounts.viewsets.mixins import PatientInfoMixin
from ..models import ConsentDoc, Study, StudyInvitation
from ..serializers import (
    ConsentDocSerializer, StudyCreateUpdateSerializer, StudyListSerializer)


class ConsentDocViewSet(viewsets.GenericViewSet,
                        mixins.CreateModelMixin):
    queryset = ConsentDoc.objects.all()
    serializer_class = ConsentDocSerializer
    permission_classes = (IsCoordinator,)


class StudyViewSet(viewsets.GenericViewSet, PatientInfoMixin,
                   mixins.CreateModelMixin, mixins.UpdateModelMixin,
                   mixins.ListModelMixin, mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin):
    queryset = Study.objects.all()
    serializer_class = StudyListSerializer
    permission_classes = (IsDoctor,)

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return StudyCreateUpdateSerializer
        else:
            return self.serializer_class

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsCoordinator()]
        elif self.action == 'add_doctor':
            return [IsCoordinatorOfDoctor()]
        else:
            return super(StudyViewSet, self).get_permissions()

    @detail_route(methods=['POST'])
    def add_doctor(self, request, pk):
        study = self.get_object()
        doctor = get_object_or_404(Doctor, pk=self.request.data['doctor_pk'])
        email_list = self.request.data['emails']
        fail_emails = {}

        for email in email_list:
            check_doctor = Doctor.objects.filter(email=email).first()
            if check_doctor and not is_participant(check_doctor):
                fail_emails.update({email: 'user is already doctor or coordinator'})
            else:
                if StudyInvitation.objects.filter(email=email, study=study).exists():
                    fail_emails.update({email: 'user is already participating'})
                else:
                    StudyInvitation.objects.create(
                        email=email,
                        study=study,
                        doctor=doctor)

        return Response({
            'all_success': len(fail_emails) == 0,
            'fail_emails': fail_emails
        })
