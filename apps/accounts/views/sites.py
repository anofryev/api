from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..models import Site


@api_view(['GET'])
@permission_classes((AllowAny, ))
def sites_view(request):
    return Response(Site.objects.values('pk', 'title'))
