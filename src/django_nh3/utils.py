import logging
from collections.abc import Callable
from typing import Any

from django.conf import settings
from django.utils.module_loading import import_string

logger = logging.getLogger(__name__)


def get_nh3_configured_default_options() -> dict[str, Any]:
    """
    Pull the django-nh3 settings similarly to how django-bleach handled them.

    Some django-bleach settings can be mapped to django-nh3 settings without
    any changes:

        BLEACH_ALLOWED_TAGS         -> NH3_ALLOWED_TAGS
        BLEACH_ALLOWED_ATTRIBUTES   -> NH3_ALLOWED_ATTRIBUTES
        BLEACH_STRIP_COMMENTS       -> NH3_STRIP_COMMENTS
        BLEACH_ALLOWED_PROTOCOLS    -> NH3_ALLOWED_URL_SCHEMES

    While other settings have no current support in nh3:

        BLEACH_ALLOWED_STYLES       -> There is no support for styling
        BLEACH_STRIP_TAGS           -> This is the default behavior of nh3

    """

    nh3_settings = {
        # Sets the tags that are allowed (eg: allowlist)
        # Ensure that no tags in this are also in NH3_CLEAN_CONTENT_TAGS or
        # NH3_ALLOWED_ATTRIBUTES
        "NH3_ALLOWED_TAGS": "tags",
        # Sets the tags whose contents will be completely removed from the
        # output (eg: blocklist)
        # Ensure that no tags in this are also in NH3_ALLOWED_TAGS or
        # NH3_ALLOWED_ATTRIBUTES
        # Default: script, style
        "NH3_ALLOWED_ATTRIBUTES": "attributes",
        # Sets the HTML attributes that are allowed on specific tags, * key
        # means the attributes are allowed on any tag (eg: allowlist)
        # Ensure that no tags in this are also in NH3_CLEAN_CONTENT_TAGS
        "NH3_CLEAN_CONTENT_TAGS": "clean_content_tags",
        # Dotted path to a callback that allows rewriting of all attributes.
        # The callback takes name of the element, attribute and its value.
        # Returns None to remove the attribute, or a value to use
        "NH3_ALLOWED_ATTRIBUTES_FILTER": "attribute_filter",
        # Configures the handling of HTML comments, defaults to True
        "NH3_STRIP_COMMENTS": "strip_comments",
        # Configures a rel attribute that will be added on links, defaults to
        # noopener noreferrer. To turn on rel-insertion, pass a space-separated
        # list. If rel is in the generic or tag attributes, this must be set to
        # None
        # Common rel values to include:
        # noopener
        # noreferrer
        # nofollow
        "NH3_LINK_REL": "link_rel",
        # Sets the prefix of attributes that are allowed on any tag
        "NH3_ALLOWED_GENERIC_ATTRIBUTE_PREFIXES": "generic_attribute_prefixes",
        # Sets the values of HTML attributes that are allowed on specific tags.
        # The value is structured as a map from tag names to a map from
        # attribute names to a set of attribute values. If a tag is not itself
        # whitelisted, adding entries to this map will do nothing.
        "NH3_ALLOWED_TAG_ATTRIBUTE_VALUES": "tag_attribute_values",
        # Sets the values of HTML attributes that are to be set on specific
        # tags. The value is structured as a map from tag names to a map from
        # attribute names to an attribute value. If a tag is not itself
        # whitelisted, adding entries to this map will do nothing.
        "NH3_SET_TAG_ATTRIBUTE_VALUES": "set_tag_attribute_values",
        # Sets the URL schemes permitted on href and src attributes
        "NH3_ALLOWED_URL_SCHEMES": "url_schemes",
    }

    return {
        kwarg: getattr(settings, setting_name)
        for setting_name, kwarg in nh3_settings.items()
        if hasattr(settings, setting_name)
    }


def normalize_nh3_options(  # noqa: C901, PLR0912
    options: dict[str, Any],
) -> dict[str, Any]:
    nh3_args: dict[str, Any] = {}
    for kwarg_name, kwarg_value in options.items():
        value = kwarg_value

        # Convert from general iterables to sets
        if kwarg_name in [
            "tags",
            "clean_content_tags",
            "generic_attribute_prefixes",
            "url_schemes",
        ]:
            value = set(value)

        elif kwarg_name == "attributes":
            copy_dict = value.copy()
            for tag, attributes in value.items():
                copy_dict[tag] = set(attributes)
            value = copy_dict

        elif kwarg_name == "attribute_filter":
            if callable(value):
                pass
            elif isinstance(value, str):
                value = import_string(value)

        elif kwarg_name == "strip_comments":
            value = bool(value)

        elif kwarg_name == "link_rel":
            value = str(value)

        elif kwarg_name == "tag_attribute_values":
            # The value is structured as a map from tag names to a map from
            # attribute names to a set of attribute values.
            allowed_tag_attr_dict: dict[str, dict[str, set[str]]] = {}
            for tag_name, attribute_dict in value.items():
                allowed_tag_attr_dict[tag_name] = {}
                for attr_name, attr_value in attribute_dict.items():
                    allowed_tag_attr_dict[tag_name][attr_name] = set(attr_value)
            value = allowed_tag_attr_dict

        elif kwarg_name == "set_tag_attribute_values":
            # The value is structured as a map from tag names to a map from
            # attribute names to an attribute value.
            set_tag_attr_dict: dict[str, dict[str, str]] = {}
            for tag_name, attribute_dict in value.items():
                set_tag_attr_dict[tag_name] = {}
                for attr_name, attr_value in attribute_dict.items():
                    set_tag_attr_dict[tag_name][attr_name] = str(attr_value)
            value = set_tag_attr_dict

        nh3_args[kwarg_name] = value

    return nh3_args


def get_nh3_default_options() -> dict[str, Any]:
    return normalize_nh3_options(get_nh3_configured_default_options())


def get_nh3_options(
    tags: set[str] | None = None,
    clean_content_tags: set[str] | None = None,
    attributes: dict[str, set[str]] | None = None,
    attribute_filter: Callable[[str, str, str], str] | None = None,
    strip_comments: bool = False,
    link_rel: str = "",
    generic_attribute_prefixes: set[str] | None = None,
    tag_attribute_values: dict[str, dict[str, set[str]]] | None = None,
    set_tag_attribute_values: dict[str, dict[str, str]] | None = None,
    url_schemes: set[str] | None = None,
) -> dict[str, Any]:
    defaults = get_nh3_configured_default_options()

    tags = tags or defaults.get("tags", None) or set()
    attributes = attributes or defaults.get("attributes", {})
    clean_content_tags = (
        clean_content_tags or defaults.get("clean_content_tags", None) or set()
    )
    attribute_filter = attribute_filter or defaults.get("attribute_filter", None)
    strip_comments = strip_comments or defaults.get("strip_comments", False)
    link_rel = link_rel or defaults.get("link_rel", "")
    generic_attribute_prefixes = (
        generic_attribute_prefixes
        or defaults.get("generic_attribute_prefixes", None)
        or set()
    )
    tag_attribute_values = (
        tag_attribute_values or defaults.get("tag_attribute_values", None) or {}
    )
    set_tag_attribute_values = (
        set_tag_attribute_values or defaults.get("set_tag_attribute_values", None) or {}
    )
    url_schemes = url_schemes or defaults.get("url_schemes", None) or set()

    return normalize_nh3_options(
        {
            "tags": tags,
            "clean_content_tags": clean_content_tags,
            "attributes": attributes,
            "attribute_filter": attribute_filter,
            "strip_comments": strip_comments,
            "link_rel": link_rel,
            "generic_attribute_prefixes": generic_attribute_prefixes,
            "tag_attribute_values": tag_attribute_values,
            "set_tag_attribute_values": set_tag_attribute_values,
            "url_schemes": url_schemes,
        }
    )
