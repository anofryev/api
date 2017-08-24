from django.db import transaction
from rest_framework import (viewsets, mixins, pagination,
                            filters, response, status, )

from ..serializers import PatientSerializer, CreatePatientSerializer
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

    def get_serializer_class(self):
        if self.action == 'create':
            return CreatePatientSerializer
        return self.serializer_class

    def get_queryset(self):
        qs = super(PatientViewSet, self).get_queryset()

        qs = qs.annotate_last_upload().annotate_moles_images_count()
        qs = qs.filter(doctors=self.request.user.doctor_role)

        return qs

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        data = PatientSerializer(
            instance=instance,
            context=self.get_serializer_context()).data
        headers = self.get_success_headers(data)

        return response.Response(
            data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
