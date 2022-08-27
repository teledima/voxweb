from django.contrib import admin
from .models import News, Tag


@admin.register(News)
class AdminNews(admin.ModelAdmin):
    list_display = ['title', 'description', 'dt', 'source', 'tags_list']
    list_filter = ['dt', 'source', ('tags__name', admin.AllValuesFieldListFilter)]
    ordering = ['-dt']
    exclude = ['uid']

    @admin.display(description='tags', empty_value='EMPTY')
    def tags_list(self, obj):
        return ', '.join([tag.name for tag in obj.tags.all()])


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    list_display = ['name']
    ordering = ['name']
    exclude = ['uid']
    pass
# Register your models here.
