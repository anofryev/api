import json
from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer

from ..models import Mole, MoleImage
from .anatomical_site import AnatomicalSiteSerializer
from .patient_anatomical_site import PatientAnatomicalSiteSerializer
from .mole_image import MoleImageSerializer


class MoleSerializer(serializers.ModelSerializer):
    anatomical_sites = AnatomicalSiteSerializer(many=True, read_only=True)
    position_info = serializers.JSONField()

    class Meta:
        model = Mole


class MoleListSerializer(MoleSerializer):
    last_image = MoleImageSerializer(read_only=True)
    images_count = serializers.IntegerField(
        source='images.count', read_only=True)

    class Meta(MoleSerializer.Meta):
        fields = ('pk', 'anatomical_sites', 'last_image', 'images_count',
                  'position_info', 'patient_anatomical_site', )


class MoleDetailSerializer(MoleSerializer):
    patient_anatomical_site = PatientAnatomicalSiteSerializer(read_only=True)
    images = MoleImageSerializer(many=True, read_only=True)

    class Meta(MoleSerializer.Meta):
        fields = ('pk', 'anatomical_sites', 'patient_anatomical_site',
                  'position_info', 'images', )


def validate_position_info(self, value):
    try:
        return json.loads(value)
    except Exception as err:
        raise serializers.ValidationError(str(err))


def validate(self, data):
    if data.get('patient_anatomical_site') is None or\
            data['patient_anatomical_site'].anatomical_site.pk \
            == data['anatomical_site'].pk:
        return data
    else:
        raise serializers.ValidationError(
            "Distant photo anatomical site missmatch mole's anatomical site")


class MoleCreateSerializer(MoleSerializer):
    photo = VersatileImageFieldSerializer(
        sizes='main_set', required=True, write_only=True)

    class Meta(MoleSerializer.Meta):
        fields = ('anatomical_site', 'patient_anatomical_site',
                  'position_info', 'photo', )

    validate_position_info = validate_position_info
    validate = validate

    def create(self, validated_data):
        photo = validated_data.pop('photo')

        mole = super(MoleCreateSerializer, self).create(validated_data)

        MoleImage.objects.create(mole=mole, photo=photo)

        return mole


class MoleUpdateSerializer(MoleSerializer):
    validate_position_info = validate_position_info
    validate = validate

    class Meta(MoleSerializer.Meta):
        fields = ('pk', 'anatomical_site',
                  'patient_anatomical_site', 'position_info', )
