from rest_framework import serializers

from news_site.models import *


class NewsSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = News
        fields = ['uid', 'title', 'description', 'dt', 'tags', 'source']
