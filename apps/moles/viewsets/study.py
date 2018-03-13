from rest_framework import viewsets, mixins
from rest_framework.decorators import detail_route

from apps.accounts.permissions import IsCoordinator, IsDoctor, IsDoctorOfPatient
from apps.accounts.viewsets.mixins import PatientInfoMixin
from apps.moles.permissions import IsMemberOfStudy
from ..models import ConsentDoc, Study, StudyToPatient
from ..serializers import ConsentDocSerializer, StudySerializer, \
    StudyListSerializer


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
    serializer_class = StudySerializer
    permission_classes = (IsDoctor,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return StudyListSerializer
        else:
            return self.serializer_class

    def get_permissions(self):
        if self.action in ['create', 'update']:
            return [IsCoordinator()]
        elif self.action == 'patient_sign':
            return [IsDoctorOfPatient(), IsMemberOfStudy()]
        else:
            return super(StudyViewSet, self).get_permissions()

    @detail_route(methods=['PUT'])
    def patient_sign(self):
        patient = self.get_patient()
        # TODO
