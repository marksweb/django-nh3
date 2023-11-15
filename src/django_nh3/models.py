from __future__ import annotations

from collections.abc import Callable
from typing import Any

import nh3
from django.db import models
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models import Expression, Model
from django.forms import Field as FormField
from django.utils.safestring import mark_safe

from . import forms


class Nh3Field(models.TextField):
    def __init__(
        self,
        attributes: dict[str, set[str]] = {},
        attribute_filter: Callable[[str, str, str], str] | None = None,
        clean_content_tags: set[str] = set(),
        link_rel: str = "",
        strip_comments: bool = False,
        tags: set[str] = set(),
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.nh3_options = {
            "attributes": attributes,
            "attribute_filter": attribute_filter,
            "clean_content_tags": clean_content_tags,
            "link_rel": link_rel,
            "strip_comments": strip_comments,
            "tags": tags,
        }

    def formfield(
        self, form_class: FormField = forms.Nh3Field, **kwargs: Any
    ) -> FormField:
        """Makes the field for a ModelForm"""

        # If field doesn't have any choices add kwargs expected by BleachField.
        if not self.choices:
            kwargs.update(
                {
                    "max_length": self.max_length,
                    "attributes": self.nh3_options.get("attributes"),
                    "attribute_filter": self.nh3_options.get(
                        "attribute_filter"
                    ),
                    "clean_content_tags": self.nh3_options.get(
                        "clean_content_tags"
                    ),
                    "link_rel": self.nh3_options.get("link_rel"),
                    "strip_comments": self.nh3_options.get("strip_comments"),
                    "tags": self.nh3_options.get("tags"),
                    "required": not self.blank,
                }
            )

        return super().formfield(form_class=form_class, **kwargs)

    def pre_save(self, model_instance: Model, add: bool) -> Any:
        data = getattr(model_instance, self.attname)
        if data is None:
            return data
        clean_value = nh3.clean(data, **self.nh3_options) if data else ""
        setattr(model_instance, self.attname, mark_safe(clean_value))
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
