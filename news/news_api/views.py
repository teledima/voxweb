from rest_framework.generics import ListAPIView
from django_filters import rest_framework as filters

from news_site.models import News
from .serializers import NewsSerializer
from .filters import NewsFilter


class NewsList(ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = NewsFilter
