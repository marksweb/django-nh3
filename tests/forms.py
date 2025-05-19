from django.forms import ModelForm

from .models import (
    Nh3CharFieldContent,
    Nh3CharFieldNullableContent,
    Nh3TextFieldContent,
    Nh3TextFieldNullableContent,
)


class Nh3CharFieldContentModelForm(ModelForm):
    """NH3 test model form"""

    class Meta:
        model = Nh3CharFieldContent
        fields = ["content"]


class Nh3CharFieldNullableContentModelForm(ModelForm):
    """NH3 test model form"""

    class Meta:
        model = Nh3CharFieldNullableContent
        fields = ["choice"]


class Nh3TextFieldContentModelForm(ModelForm):
    """NH3 test model form"""

    class Meta:
        model = Nh3TextFieldContent
        fields = ["content"]


class Nh3TextFieldNullableContentModelForm(ModelForm):
    """NH3 test model form"""

    class Meta:
        model = Nh3TextFieldNullableContent
        fields = ["choice"]
