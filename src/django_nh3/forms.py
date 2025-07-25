from __future__ import annotations

from collections.abc import Callable
from typing import Any

import nh3
from django import forms
from django.utils.safestring import mark_safe

from .utils import get_nh3_options


class Nh3Field(forms.CharField):
    """nh3 form field"""

    empty_values: list[Any] = [None, "", [], (), {}]

    def __init__(
        self,
        *args: Any,
        allowed_attributes: dict[str, set[str]] | None = None,
        allowed_attribute_filter: Callable[[str, str, str], str] | None = None,
        allowed_tags: set[str] | None = None,
        clean_content_tags: set[str] | None = None,
        empty_value: Any | None = "",
        generic_attribute_prefixes: set[str] | None = None,
        link_rel: str = "",
        set_tag_attribute_values: dict[str, dict[str, str]] | None = None,
        strip_comments: bool = False,
        tag_attribute_values: dict[str, dict[str, set[str]]] | None = None,
        url_schemes: set[str] | None = None,
        **kwargs: dict[Any, Any],
    ):
        super().__init__(*args, **kwargs)

        self.empty_value = empty_value
        self.nh3_options = get_nh3_options(
            attributes=allowed_attributes,
            attribute_filter=allowed_attribute_filter,
            clean_content_tags=clean_content_tags,
            generic_attribute_prefixes=generic_attribute_prefixes,
            link_rel=link_rel,
            set_tag_attribute_values=set_tag_attribute_values,
            strip_comments=strip_comments,
            tags=allowed_tags,
            tag_attribute_values=tag_attribute_values,
            url_schemes=url_schemes,
        )

    def to_python(self, value: Any) -> Any:
        """
        Strips any dodgy HTML tags from the input if the input value
        contains HTML

        Mark the return value as template safe if it contains HTML.
        """
        value = super().to_python(value)
        if value in self.empty_values:
            # Ensures that None is handled properly as an input
            return self.empty_value
        else:
            return mark_safe(nh3.clean(value, **self.nh3_options))
