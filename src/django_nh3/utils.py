import logging
from typing import Any

from django.conf import settings

logger = logging.getLogger(__name__)


def get_nh3_default_options() -> dict[str, Any]:
    """
    Pull the django-nh3 settings similarly to how django-bleach handled them.

    Some django-bleach settings can be mapped to django-nh3 settings without
    any changes:

        BLEACH_ALLOWED_TAGS         -> NH3_ALLOWED_TAGS
        BLEACH_ALLOWED_ATTRIBUTES   -> NH3_ALLOWED_ATTRIBUTES
        BLEACH_STRIP_COMMENTS       -> NH3_STRIP_COMMENTS

    While other settings are have no current support in nh3:

        BLEACH_ALLOWED_STYLES       -> There is no support for styling
        BLEACH_ALLOWED_PROTOCOLS    -> There is no suport for protocols
        BLEACH_STRIP_TAGS           -> This is the default behavior of nh3

    """
    nh3_args: dict[str, Any] = {}

    nh3_settings = {
        "NH3_ALLOWED_TAGS": "tags",
        "NH3_ALLOWED_ATTRIBUTES": "attributes",
        "NH3_STRIP_COMMENTS": "strip_comments",
    }

    for setting, kwarg in nh3_settings.items():
        if hasattr(settings, setting):
            attr = getattr(settings, setting)

            # Convert from general iterables to sets
            if setting == "NH3_ALLOWED_TAGS":
                attr = set(attr)
            elif setting == "NH3_ALLOWED_ATTRIBUTES":
                copy_dict = attr.copy()
                for tag, attributes in attr.items():
                    copy_dict[tag] = set(attributes)
                attr = copy_dict

            nh3_args[kwarg] = attr

    return nh3_args
