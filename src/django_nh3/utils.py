import logging
from typing import Any

from django.conf import settings

logger = logging.getLogger(__name__)


def get_nh3_default_options() -> dict[str | None, Any]:
    nh3_args = {}
    nh3_settings = {
        "NH3_ALLOWED_TAGS": "tags",
        "NH3_ALLOWED_ATTRIBUTES": "attributes",
        "NH3_STRIP_COMMENTS": "strip_comments",
    }

    bleach_to_nh3_mapping = {
        "BLEACH_ALLOWED_TAGS": nh3_settings["NH3_ALLOWED_TAGS"],
        "BLEACH_ALLOWED_ATTRIBUTES": nh3_settings["NH3_ALLOWED_ATTRIBUTES"],
        "BLEACH_STRIP_COMMENTS": nh3_settings["NH3_STRIP_COMMENTS"],
    }

    unsupported_bleach_tags = {
        "BLEACH_ALLOWED_STYLES": None,
        "BLEACH_ALLOWED_PROTOCOLS": None,
        "BLEACH_STRIP_TAGS": None,
    }

    for setting, kwarg in {
        **nh3_settings,
        **bleach_to_nh3_mapping,
        **unsupported_bleach_tags,
    }.items():
        if hasattr(settings, setting):
            attr = getattr(settings, setting)

            if setting == "BLEACH_STRIP_TAGS":
                if attr is True:
                    logger.info(
                        'Legacy bleach setting "BLEACH_STRIP_TAGS=True" is '
                        "unneeded as nh3 will always strip unallowed content."
                    )
                else:
                    logger.warning(
                        f'Legacy bleach setting "BLEACH_STRIP_TAGS={attr}" is'
                        " unsupported and will be ignored as nh3 will always "
                        "strip unallowed content."
                    )

                continue

            if setting in unsupported_bleach_tags:
                logger.warning(
                    f'Legacy bleach setting "{setting}" is not currently '
                    "supported by nh3 and will be ignored."
                )
                continue

            # Convert the iterable format of BLEACH_ALLOWED_ATTRIBUTES
            # & BLEACH_ALLOWED_TAGS to that of nh3
            if setting == "BLEACH_ALLOWED_ATTRIBUTES":
                attr = {"*", set(attr)}
            elif setting == "BLEACH_ALLOWED_TAGS":
                attr = set(attr)

            nh3_args[kwarg] = attr

    return nh3_args
