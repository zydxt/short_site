# coding=utf-8
from django.test import TestCase
from django.conf import settings
from django.http import Http404
from short_url.forms import ShortURLForm
from short_url.services import generate_short_url, get_redirect_url
from short_url.models import ShortUrl


class TestGenerateShortUrl(TestCase):

    def setUp(self):
        ShortUrl(origin_url="http://www.example.com",
                 short_key="B",
                 is_custom=False).save()

    def test_simple_generate_short_url(self):
        result = generate_short_url(ShortURLForm({"origin_url": "http://www.example.com"}))
        self.assertEqual(result, {"success": True,
                                  "msg": "获得的短链接是%s%s" % (settings.SITE_PREFIX, "C")})
        self.assertTrue(ShortUrl.objects.filter(origin_url="http://www.example.com",
                                                short_key="C", is_custom=False).exists())

        result = generate_short_url(ShortURLForm({"origin_url": ""}))
        self.assertFalse(result["success"])

    def test_generate_short_url_with_custom_key(self):
        result = generate_short_url(ShortURLForm({"origin_url": "http://www.customkey.com",
                                                  "custom_key": "B"}))
        self.assertFalse(result["success"])

        result = generate_short_url(ShortURLForm({"origin_url": "http://www.customkey.com",
                                                  "custom_key": "C"}))
        self.assertTrue(ShortUrl.objects.filter(origin_url="http://www.customkey.com",
                                                short_key="C", is_custom=True).exists())
        self.assertEqual(result, {"success": True,
                                  "msg": "获得的短链接是%s%s" % (settings.SITE_PREFIX, "C")})

    def test_generate_short_url_with_key_occupied_once(self):
        ShortUrl(origin_url="http://www.example.com",
                 short_key="D",
                 is_custom=True).save()
        result = generate_short_url(ShortURLForm({"origin_url": "http://www.example.com"}))
        self.assertEqual(result, {"success": True,
                                  "msg": "获得的短链接是%s%s" % (settings.SITE_PREFIX, "C")})
        # normally when pk=3 short_key should be D but now it should be C
        self.assertTrue(ShortUrl.objects.filter(pk=3, short_key="C", is_custom=False).exists())

    def test_generate_short_url_with_key_occupied_twice(self):
        ShortUrl(origin_url="http://www.example.com",
                 short_key="E",
                 is_custom=True).save()  # id = 2
        ShortUrl(origin_url="http://www.example.com",
                 short_key="C",
                 is_custom=True).save()  # id = 3
        result = generate_short_url(ShortURLForm({"origin_url": "http://www.example.com"}))
        self.assertEqual(result, {"success": True,
                                  "msg": "获得的短链接是%s%s" % (settings.SITE_PREFIX, "D")})
        # normally when pk=4 short_key should be E but now it should be D
        self.assertTrue(ShortUrl.objects.filter(pk=4, short_key="D", is_custom=False).exists())


class TestGetRedirectUrl(TestCase):

    def setUp(self):
        self.short_url = ShortUrl(origin_url="http://www.example.com",
                                  short_key="B",
                                  is_custom=False)
        self.short_url.save()

    def test_get_redirect_url(self):
        redirect_url = get_redirect_url("B")
        self.assertEqual(redirect_url, self.short_url.origin_url)

        self.assertRaises(Http404, get_redirect_url, "C")
