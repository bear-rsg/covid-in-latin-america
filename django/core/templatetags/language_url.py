from django import template

register = template.Library()


@register.simple_tag
def language_url(lang_code, url):
    """
    Build a new url that includes the provided lang_code by replacing
    the language code in the provided URL with the provided lang_code

    e.g. if url is "/es/objects/2/" and lang_code is "en"
    then new url is "/en/objects/2/"
    """
    return f"/{lang_code}/{'/'.join(url.split('/')[2:])}"
