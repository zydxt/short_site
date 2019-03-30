# coding=utf-8

from django.db import models
from django.db.models.signals import post_save


class ShortUrl(models.Model):
    origin_url = models.URLField(verbose_name="原始url", max_length=2083)
    short_key = models.CharField(verbose_name="短链接key", max_length=10, unique=True, null=True)
    is_custom = models.BooleanField(verbose_name="是否自定义", default=False)


class ViewCount(models.Model):

    short_url = models.OneToOneField(ShortUrl, on_delete=models.PROTECT, related_name='view_count')
    view_count = models.IntegerField(verbose_name='访问计数', default=0)


def handle_create_short_url(sender, **kwargs):
    if sender is not ShortUrl:
        return
    created = kwargs["created"]
    instance = kwargs["instance"]
    if created:
        ViewCount(short_url=instance).save()


post_save.connect(receiver=handle_create_short_url, sender=ShortUrl)
