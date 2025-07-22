from __future__ import annotations

from collections.abc import Callable
from typing import Any

import nh3
from django import forms
from django.utils.safestring import mark_safe

from src.django_nh3.utils import get_nh3_update_options


class Nh3Field(forms.CharField):
    """nh3 form field"""

    empty_values: list[Any] = [None, "", [], (), {}]

    def __init__(
        self,
        attributes: dict[str, set[str]] | None = None,
        attribute_filter: Callable[[str, str, str], str] | None = None,
        clean_content_tags: set[str] | None = None,
        empty_value: Any | None = None,
        link_rel: str = "",
        strip_comments: bool = False,
        tags: set[str] | None = None,
        *args: Any,
        **kwargs: dict[Any, Any],
    ):
        super().__init__(*args, **kwargs)

        self.empty_value = empty_value
        self.nh3_options = get_nh3_update_options(
            attributes=attributes,
            attribute_filter=attribute_filter,
            clean_content_tags=clean_content_tags,
            link_rel=link_rel,
            strip_comments=strip_comments,
            tags=tags,
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
