from rest_framework import viewsets, mixins, pagination, filters

from ..serializers import PatientSerializer
from ..models import Patient
from ..permissions import IsDoctor
from ..filters import PatientFilter


class PatientViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin, mixins.UpdateModelMixin):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()
    permission_classes = (IsDoctor, )
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend, )
    filter_class = PatientFilter
    pagination_class = pagination.LimitOffsetPagination
    search_fields = ('first_name', 'last_name', 'mrn', )

    def get_queryset(self):
        qs = super(PatientViewSet, self).get_queryset()

        qs = qs.annotate_last_upload().annotate_moles_images_count()
        qs = qs.filter(doctor=self.request.user.doctor_role)

        return qs

    def perform_create(self, serializer):
        return serializer.save(doctor=self.request.user.doctor_role)
