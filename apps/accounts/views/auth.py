from rest_framework import serializers
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from ..models import Doctor


class CustomJSONWebTokenSerializer(JSONWebTokenSerializer):
    def validate(self, attrs):
        errors = []
        if Doctor.objects.filter(
                username=attrs.get('username', None),
                approved_by_coordinator=False).exists():
            errors.append("Account is not approved by your coordinator")
        if Doctor.objects.filter(
                username=attrs.get('username', None),
                is_active=False).exists():
            errors.append("Account is not activated")

        if errors != []:
            raise serializers.ValidationError(errors)

        return super(CustomJSONWebTokenSerializer, self).validate(attrs)


class ObtainJSONWebToken(JSONWebTokenAPIView):
    serializer_class = CustomJSONWebTokenSerializer


obtain_jwt_token = ObtainJSONWebToken.as_view()
