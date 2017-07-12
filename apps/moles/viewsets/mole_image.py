from rest_framework import viewsets, mixins

from apps.accounts.permissions import (
    C, IsDoctorOfPatient, HasPatientValidConsent, AllowAllExceptCreation)
from ..models import Mole, MoleImage
from ..serializers import (
    MoleImageSerializer, MoleImageCreateSerializer, MoleImageUpdateSerializer)


class MoleImageViewSet(viewsets.GenericViewSet,
                       mixins.ListModelMixin, mixins.RetrieveModelMixin,
                       mixins.CreateModelMixin, mixins.UpdateModelMixin):
    queryset = MoleImage.objects.all()
    serializer_class = MoleImageSerializer
    permission_classes = (
        IsDoctorOfPatient,
        C(HasPatientValidConsent) | C(AllowAllExceptCreation)
    )

    def get_mole_pk(self):
        return self.kwargs['mole_pk']

    def get_mole(self):
        return Mole.objects.get(pk=self.get_mole_pk())

    def get_queryset(self):
        qs = super(MoleImageViewSet, self).get_queryset()

        return qs.filter(mole=self.get_mole_pk())

    def get_serializer_class(self):
        if self.action == 'create':
            return MoleImageCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return MoleImageUpdateSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        return serializer.save(mole=self.get_mole())
