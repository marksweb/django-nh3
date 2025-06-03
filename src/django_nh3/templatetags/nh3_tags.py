import nh3
from django import template
from django.utils.safestring import SafeText, mark_safe

from django_nh3.utils import get_nh3_default_options

register = template.Library()


@register.filter(name="nh3")
def nh3_value(value: str | None, allowed_tags: str | None = None) -> SafeText | None:
    """
    Takes an input HTML value and sanitizes it utilizing nh3,
        returning a SafeText object that can be rendered by Django.

    Accepts an optional argument of allowed tags. Should be a comma delimited
        string (i.e. "img,span" or "img")
    """
    if value is None:
        return None

    nh3_args = get_nh3_default_options()
    if allowed_tags is not None:
        args = nh3_args.copy()
        args["tags"] = set(allowed_tags.split(","))
    else:
        args = nh3_args

    clean_value = nh3.clean(value, **args)
    return mark_safe(clean_value)
