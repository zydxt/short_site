# coding=utf-8
from django.db.models import F
from django.http import Http404
from django.conf import settings
from .models import ShortUrl, ViewCount
from .baseconverter import base62


def generate_short_url(short_form):
    if not short_form.is_valid():
        return {"success": False, "msg": "请输入正确的参数"}

    origin_url = short_form.cleaned_data["origin_url"]
    custom_key = short_form.cleaned_data["custom_key"]
    if custom_key and ShortUrl.objects.filter(short_key=custom_key).exists():
        return {"success": False, "msg": "自定义Key已存在，请更换重试"}

    short_url_obj = ShortUrl(origin_url=origin_url)
    short_url_obj.save()

    if custom_key:
        short_url_obj.short_key = custom_key
        short_url_obj.is_custom = True
        short_url_obj.save()
    else:
        short_key = base62.from_decimal(short_url_obj.id)
        exists_obj = ShortUrl.objects.filter(short_key=short_key, is_custom=True).first()
        while exists_obj:
            # 被自定义key占用，将自定义记录的id转换成新生成记录的key, 该key也可能被占用，应继续查找直到不被占用为止
            short_key = base62.from_decimal(exists_obj.id)
            exists_obj = ShortUrl.objects.filter(short_key=short_key, is_custom=True).first()

        short_url_obj.short_key = short_key
        short_url_obj.save()
    return {"success": True, "msg": "获得的短链接是%s%s" % (settings.SITE_PREFIX, short_url_obj.short_key)}


def get_redirect_url(short_key):
    short_url_obj = ShortUrl.objects.filter(short_key=short_key).first()
    if not short_url_obj:
        raise Http404("Page Not Found")
    ViewCount.objects.filter(short_url=short_url_obj).update(view_count=F("view_count") + 1)
    return short_url_obj.origin_url
