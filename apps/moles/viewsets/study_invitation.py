from rest_framework import viewsets, mixins
from rest_framework.decorators import detail_route

from apps.accounts.permissions import IsDoctor
from ..models import Study, StudyInvitation
from ..serializers import StudyInvitationSerializer


class StudyInvitationViewSet(viewsets.GenericViewSet,
                             mixins.ListModelMixin):
    queryset = StudyInvitation.objects.all()
    serializer_class = StudyInvitationSerializer
    permission_classes = (IsDoctor,)

    def get_study_pk(self):
        return self.kwargs['study_pk']

    def get_study(self):
        return Study.objects.get(pk=self.get_study_pk())

    def get_queryset(self):
        qs = super(StudyInvitationViewSet, self).get_queryset()
        return qs.filter(
            email=self.request.user.doctor_role__email,
            study=self.get_study_pk())

    @detail_route(methods=['POST'])
    def approve(self):
        invitation = self.get_object()
        pass

    @detail_route(methods=['POST'])
    def decline(self):
        invitation = self.get_object()
        pass
