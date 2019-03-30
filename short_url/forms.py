# coding=utf-8
from django.forms import Form, URLField, CharField
from django.core.validators import RegexValidator


class ShortURLForm(Form):
    origin_url = URLField(label="原始地址", max_length=2083, required=True)
    custom_key = CharField(label="自定义key", min_length=1, max_length=7, required=False,
                           validators=(RegexValidator(r'^[0-9A-Za-z]{1,7}$', message=u"自定义Key必须是1-7位字母数字"),))
