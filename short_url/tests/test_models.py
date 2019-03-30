# coding=utf-8

from django.test import TestCase
from django.db.utils import IntegrityError
from short_url.models import ShortUrl, ViewCount


class TestShortUrl(TestCase):

    def test_create_short_url(self):
        new_obj = ShortUrl(origin_url='http://example.com/',
                           short_key='B',
                           is_custom=False)
        new_obj.save()
        # Should auto create ViewCount record
        self.assertTrue(ViewCount.objects.filter(short_url=new_obj, view_count=0).exists())

        # Should Raise IntegrityError
        self.assertRaises(IntegrityError, ShortUrl(origin_url='http://example.com/',
                                                   short_key='B',
                                                   is_custom=True).save)
