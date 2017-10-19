from rest_framework import serializers

from ..models import SiteJoinRequest
from .doctor import DoctorSerializer


class CreateSiteJoinRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteJoinRequest
        fields = ('pk', 'site', )

    def validate(self, validated_data):
        if SiteJoinRequest.objects.filter(
                site=validated_data['site'],
                doctor_id=self.context['request'].user.id).exists():
            raise serializers.ValidationError(
                "You have already requested joining to {0}".format(
                    validated_data['site']))
        return validated_data

    def create(self, validated_data):
        validated_data['doctor_id'] = self.context['request'].user.id
        return super(CreateSiteJoinRequestSerializer,
                     self).create(validated_data)


class SiteJoinRequestSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()

    class Meta:
        model = SiteJoinRequest
        fields = ('pk', 'doctor', 'state', 'date_created', 'date_modified', )
