import django_filters

from news_site.models import News, Tag

SOURCE_CHOICE = (('yandex', 'yandex'), ('ozon', 'ozon'))


class NewsFilter(django_filters.FilterSet):
    source = django_filters.CharFilter()
    dt = django_filters.DateFromToRangeFilter()
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__name',
        to_field_name='name',
        null_label='EMPTY',
        null_value='EMPTY',
        queryset=Tag.objects.all()
    )

    class Meta:
        model = News
        fields = ['source', 'dt', 'tags']
