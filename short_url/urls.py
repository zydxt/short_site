# coding=utf-8
from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.ShortURL.as_view(), name='index'),
    re_path('^(?P<short_key>[0-9A-Za-z]{1,7})/$', views.ShortUrlRedirect.as_view(), name='short-url-redirect'),
    re_path('^(?P<short_key>[0-9A-Za-z]{1,7})/view_count/$', views.UrlViewCount.as_view(), name='short-url-view-count'),
]
