from urllib.parse import urlparse

from django import template

register = template.Library()


@register.simple_tag
def url_path(complete_url):
    return urlparse(complete_url).path
