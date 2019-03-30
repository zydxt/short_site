# coding=utf-8
from django.test import TestCase
from short_url.forms import ShortURLForm


class TestShortURLForm(TestCase):

    def test_validate_url(self):
        self.assertTrue(ShortURLForm({"origin_url": "http://www.example.com/"}).is_valid())

        self.assertTrue(ShortURLForm({"origin_url": "https://www.example.com/"}).is_valid())

        self.assertFalse(ShortURLForm({"origin_url": ""}).is_valid())

    def test_validate_custom_key(self):

        self.assertTrue(ShortURLForm({"origin_url": "http://www.example.com/",
                                      "custom_key": ""}).is_valid())
        self.assertFalse(ShortURLForm({"origin_url": "http://www.example.com/",
                                      "custom_key": "2Bhj*"}).is_valid())
        self.assertFalse(ShortURLForm({"origin_url": "http://www.example.com/",
                                      "custom_key": "2BhjiUjwi"}).is_valid())

