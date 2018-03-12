from rest_framework import viewsets, mixins

from apps.accounts.permissions import IsCoordinator, IsDoctor
from ..models import ConsentDoc, Study
from ..serializers import ConsentDocSerializer, StudySerializer, \
    StudyListSerializer


class ConsentDocViewSet(viewsets.GenericViewSet,
                        mixins.CreateModelMixin):
    queryset = ConsentDoc.objects.all()
    serializer_class = ConsentDocSerializer
    permission_classes = (IsCoordinator,)


class StudyViewSet(viewsets.GenericViewSet,
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
        else:
            return super(StudyViewSet, self).get_permissions()
