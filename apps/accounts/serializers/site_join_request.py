from rest_framework import serializers

from ..models import SiteJoinRequest, Doctor
from .doctor import DoctorFullSerializer


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
    doctor = DoctorFullSerializer()
    site_title = serializers.CharField(source='site.title')
    coordinator_public_key = serializers.SerializerMethodField()

    def get_coordinator_public_key(self, obj):
        return Doctor.objects.get(
            id=obj.site.site_coordinator_id).public_key

    class Meta:
        model = SiteJoinRequest
        fields = ('pk', 'doctor', 'state', 'coordinator_public_key',
                  'date_created', 'date_modified', 'site_title', )
