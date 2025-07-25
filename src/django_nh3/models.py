from __future__ import annotations

import warnings
from collections.abc import Callable
from typing import Any

import nh3
from django.db import models
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models import Expression, Model
from django.forms import Field as FormField
from django.utils.safestring import mark_safe
from typing_extensions import deprecated

from . import forms
from .utils import get_nh3_options


class Nh3FieldMixin:
    def __init__(
        self,
        *args: Any,
        allowed_attributes: dict[str, set[str]] | None = None,
        allowed_attribute_filter: Callable[[str, str, str], str] | None = None,
        allowed_tags: set[str] | None = None,
        clean_content_tags: set[str] | None = None,
        generic_attribute_prefixes: set[str] | None = None,
        link_rel: str = "",
        set_tag_attribute_values: dict[str, dict[str, str]] | None = None,
        strip_comments: bool = False,
        tag_attribute_values: dict[str, dict[str, set[str]]] | None = None,
        url_schemes: set[str] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)

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

    def formfield(
        self, form_class: FormField = forms.Nh3Field, **kwargs: Any
    ) -> FormField:
        """Makes the field for a ModelForm"""

        # If field doesn't have any choices add kwargs expected by Nh3Field.
        if not self.choices:  # type: ignore[attr-defined]
            kwargs.update(
                {
                    "allowed_attributes": self.nh3_options.get("attributes"),
                    "allowed_attribute_filter": self.nh3_options.get(
                        "attribute_filter"
                    ),
                    "allowed_tags": self.nh3_options.get("tags"),
                    "clean_content_tags": self.nh3_options.get("clean_content_tags"),
                    "generic_attribute_prefixes": self.nh3_options.get(
                        "generic_attribute_prefixes"
                    ),
                    "link_rel": self.nh3_options.get("link_rel"),
                    "max_length": self.max_length,  # type: ignore[attr-defined]
                    "required": not self.blank,  # type: ignore[attr-defined]
                    "set_tag_attribute_values": self.nh3_options.get(
                        "set_tag_attribute_values"
                    ),
                    "strip_comments": self.nh3_options.get("strip_comments"),
                    "tag_attribute_values": self.nh3_options.get(
                        "tag_attribute_values"
                    ),
                    "url_schemes": self.nh3_options.get("url_schemes"),
                }
            )

        return super().formfield(form_class=form_class, **kwargs)  # type: ignore[misc]

    def pre_save(self, model_instance: Model, add: bool) -> Any:
        data = getattr(model_instance, self.attname)  # type: ignore[attr-defined]
        if data is None:
            return data
        clean_value = nh3.clean(data, **self.nh3_options) if data else ""
        setattr(model_instance, self.attname, mark_safe(clean_value))  # type: ignore[attr-defined]
        return clean_value

    def from_db_value(
        self,
        value: Any,
        expression: Expression,
        connection: BaseDatabaseWrapper,
    ) -> Any:
        if value is None:
            return value
        # Values are sanitised before saving, so any value returned from the DB
        # is safe to render unescaped.
        return mark_safe(value)


class Nh3TextField(Nh3FieldMixin, models.TextField):
    pass


class Nh3CharField(Nh3FieldMixin, models.CharField):
    pass


@deprecated("Use Nh3TextField instead")
class Nh3Field(Nh3FieldMixin, models.TextField):
    """
    .. deprecated:: 0.2.0
    Use :class:`Nh3TextField` instead.
    """

    def __init__(self, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        warnings.warn(
            "Nh3Field is deprecated and will be removed in a future version. "
            "Use Nh3TextField instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)
