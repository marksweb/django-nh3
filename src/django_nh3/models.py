from typing import Callable, Dict, Optional, Set

from django.db import models
from django.utils.safestring import mark_safe

import nh3

from . import forms


class Nh3Field(models.TextField):
    def __init__(
        self, attributes: Dict[str, Set[str]] = {},
        attribute_filter: Optional[Callable[[str, str, str], str]] = None,
        clean_content_tags: Set[str] = set(), link_rel: str = "",
        strip_comments: bool = False, tags: Set[str] = set(), *args, **kwargs
    ):

        super().__init__(*args, **kwargs)

        self.nh3_options = {
            "attributes": attributes,
            "attribute_filter": attribute_filter,
            "clean_content_tags": clean_content_tags,
            "link_rel": link_rel,
            "strip_comments": strip_comments,
            "tags": tags
        }

    def formfield(self, form_class=forms.Nh3Field, **kwargs):
        """ Makes the field for a ModelForm """

        # If field doesn't have any choices add kwargs expected by BleachField.
        if not self.choices:
            kwargs.update({
                "max_length": self.max_length,
                "attributes": self.nh3_options.get("attributes"),
                "attribute_filter": self.nh3_options.get("attribute_filter"),
                "clean_content_tags": self.nh3_options.get("clean_content_tags"),
                "link_rel": self.nh3_options.get("link_rel"),
                "strip_comments": self.nh3_options.get("strip_comments"),
                "tags": self.nh3_options.get("tags"),
                "required": not self.blank,
            })

        return super().formfield(form_class=form_class, **kwargs)

    def pre_save(self, model_instance, add):
        data = getattr(model_instance, self.attname)
        if data is None:
            return data
        clean_value = nh3.clean(data, **self.nh3_options) if data else ""
        setattr(model_instance, self.attname, mark_safe(clean_value))
        return clean_value

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        # Values are sanitised before saving, so any value returned from the DB
        # is safe to render unescaped.
        return mark_safe(value)
