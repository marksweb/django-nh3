from __future__ import annotations

from collections.abc import Callable
from typing import Any

import nh3
from django import forms
from django.utils.safestring import mark_safe


class Nh3Field(forms.CharField):
    """nh3 form field"""

    empty_values: list[Any] = [None, "", [], (), {}]

    def __init__(
        self,
        attributes: dict[str, set[str]] = {},
        attribute_filter: Callable[[str, str, str], str] | None = None,
        clean_content_tags: set[str] = set(),
        empty_value: Any | None = None,
        link_rel: str = "",
        strip_comments: bool = False,
        tags: set[str] = set(),
        *args: Any,
        **kwargs: dict[Any, Any],
    ):
        super().__init__(*args, **kwargs)

        self.empty_value = empty_value
        self.nh3_options = {
            "attributes": attributes,
            "attribute_filter": attribute_filter,
            "clean_content_tags": clean_content_tags,
            "link_rel": link_rel,
            "strip_comments": strip_comments,
            "tags": tags,
        }

    def to_python(self, value: Any) -> Any:
        """
        Strips any dodgy HTML tags from the input if the input value
        contains HTML

        Mark the return value as template safe if it contains HTML.
        """
        if value in self.empty_values:
            return self.empty_value
        if nh3.is_html(value):
            return mark_safe(nh3.clean(value, **self.nh3_options))
        else:
            return value
