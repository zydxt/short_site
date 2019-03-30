# coding=utf-8

from django.views import View
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ShortURLForm
from .services import generate_short_url, get_redirect_url
from .models import ViewCount


class ShortURL(View):
    http_method_names = {'get', 'post'}
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        data = {"short_form": ShortURLForm()}
        return render(request, self.template_name, data)

    def post(self, request, *args, **kwargs):
        short_form = ShortURLForm(request.POST)
        result = generate_short_url(short_form)
        response_data = {"result": result,
                         "short_form": short_form}
        return render(request, self.template_name, response_data)


class ShortUrlRedirect(View):
    http_method_names = {'get'}

    def get(self, request, short_key, *args, **kwargs):
        redirect_url = get_redirect_url(short_key)
        return redirect(redirect_url)


class UrlViewCount(View):
    http_method_names = {"get"}

    def get(self, request, short_key, *args, **kwargs):
        view_count_obj = get_object_or_404(ViewCount, short_url__short_key=short_key)
        return render(request, "view_count.html", {"view_count": view_count_obj.view_count})
