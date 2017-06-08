from rest_framework import serializers

from ..models import AnatomicalSite


class AnatomicalSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnatomicalSite
        fields = ('pk', 'parent', 'name', 'slug',)
