from django.db import models
from datetime import datetime

import uuid


class Tag(models.Model):
    uid = models.fields.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50, null=False, unique=True)

    class Meta:
        db_table = 'tags'

    def __str__(self):
        return f'{self.name}'


class News(models.Model):
    SourceType = models.TextChoices('SourceType', 'yandex ozon')

    uid = models.fields.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.fields.TextField(null=False)
    description = models.fields.TextField(null=True, blank=True)
    dt = models.fields.DateTimeField(default=datetime.now)
    source = models.fields.TextField(null=True, blank=True, choices=SourceType.choices, max_length=50)
    tags = models.ManyToManyField(to=Tag, db_table='news_tags', blank=True)

    class Meta:
        db_table = 'news'
        verbose_name_plural = 'news'

    def __str__(self):
        return f'{self.title}'
