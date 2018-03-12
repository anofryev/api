from rest_framework import viewsets, mixins

from apps.accounts.permissions import IsCoordinator
from ..models import ConsentDoc, Study
from ..serializers import ConsentDocSerializer, StudySerializer


class ConsentDocViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = ConsentDoc.objects.all()
    serializer_class = ConsentDocSerializer
    permission_classes = (IsCoordinator,)


class StudyViewSet(viewsets.GenericViewSet):
    pass
