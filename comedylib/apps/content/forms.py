from django import forms

from taggit.models import Tag


class CategsForm(forms.Form):
    categs = forms.MultipleChoiceField(
        label='',
        widget=forms.CheckboxSelectMultiple(),
        choices=((t.name, t.name) for t in Tag.objects.all())
    )
