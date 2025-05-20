import logging
from collections.abc import Callable
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

    While other settings have no current support in nh3:

        BLEACH_ALLOWED_STYLES       -> There is no support for styling
        BLEACH_ALLOWED_PROTOCOLS    -> There is no support for protocols
        BLEACH_STRIP_TAGS           -> This is the default behavior of nh3

    """
    nh3_args: dict[str, Any] = {}

    nh3_settings = {
        "NH3_ALLOWED_TAGS": "tags",
        "NH3_CLEAN_CONTENT_TAGS": "clean_content_tags",
        "NH3_ALLOWED_ATTRIBUTES": "attributes",
        "NH3_ALLOWED_ATTRIBUTES_FILTER": "attribute_filter",
        "NH3_STRIP_COMMENTS": "strip_comments",
        "NH3_LINK_REL": "link_rel",
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


def get_nh3_options(
    tags: set[str] | None = None,
    clean_content_tags: set[str] | None = None,
    attributes: dict[str, set[str]] | None = None,
    attribute_filter: Callable[[str, str, str], str] | None = None,
    strip_comments: bool = False,
    link_rel: str = "",
) -> dict[str, Any]:
    _tags = tags or getattr(settings, "NH3_ALLOWED_TAGS", None) or set()
    _clean_content_tags = (
        clean_content_tags or getattr(settings, "NH3_CLEAN_CONTENT_TAGS", None) or set()
    )
    _attributes = attributes or getattr(settings, "NH3_ALLOWED_ATTRIBUTES", {})
    _attribute_filter = attribute_filter or getattr(
        settings, "NH3_ALLOWED_ATTRIBUTES_FILTER", None
    )
    _strip_comments = strip_comments or getattr(settings, "NH3_STRIP_COMMENTS", False)
    _link_rel = link_rel or getattr(settings, "NH3_LINK_REL", "")

    nh3_args = {
        "tags": set(_tags),
        "clean_content_tags": set(_clean_content_tags),
        "attributes": {tag: set(attributes) for tag, attributes in _attributes.items()},
        "attribute_filter": _attribute_filter,
        "strip_comments": _strip_comments,
        "link_rel": _link_rel,
    }

    return nh3_args
