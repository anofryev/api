from rest_framework import serializers

from ..models import ConsentDoc, Study


class ConsentDocSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsentDoc


class StudySerializer(serializers.ModelSerializer):
    class Meta:
        model = Study
