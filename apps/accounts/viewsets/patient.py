from django.db import transaction
from rest_framework import (viewsets, mixins, pagination,
                            filters, response, status, )

from apps.accounts.models import Doctor
from apps.accounts.models.coordinator import is_coordinator
from apps.accounts.models.participant import is_participant
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
        study_pk = self.get_study_pk()

        result = super(PatientViewSet, self)\
            .get_queryset()\
            .annotate_last_upload()\
            .annotate_moles_count(study_pk)\
            .annotate_moles_images_count(study_pk)\
            .annotate_clinical_diagnosis_required(study_pk)\
            .annotate_pathological_diagnosis_required(study_pk)\
            .annotate_biopsy_count(study_pk)\
            .annotate_approve_required(study_pk)

        user_doctor = self.request.user.doctor_role
        if is_coordinator(user_doctor):
            result = result.filter(doctors__pk__in=Doctor.objects.filter(
                my_coordinator=user_doctor.coordinator_role
            ).values_list('pk', flat=True))
        else:
            result = result.filter(doctors=user_doctor)

        if study_pk:
            result = result.filter(studies__pk=study_pk)
        elif not is_participant(user_doctor):
            # for participant return all patients, because it will be single
            result = result.filter(studies__isnull=True)

        return result

    def get_serializer_context(self):
        result = super(PatientViewSet, self).get_serializer_context()
        result['study'] = self.get_study_pk()
        return result

    def get_study_pk(self):
        return self.request.GET.get('study') \
            if 'study' in self.request.GET else None

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
