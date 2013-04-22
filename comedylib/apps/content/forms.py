import collections

from django import forms
from django.utils.safestring import mark_safe

from taggit.models import Tag


class CheckboxSelectMultipleWithGroups(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        groups = collections.defaultdict(list)
        for categ_name, categ_val in self.choices:
            if ':' in categ_name:
                group, categ = categ_name.split(':')
                groups[group.strip()].append((categ_name, categ.strip()))
            else:
                groups[''].append((categ_name, categ_val))

        output = []
        for group, group_choices in groups.iteritems():
            output.append(u'<h3>%s</h3>' % group)
            self.choices = group_choices
            output.append(super(CheckboxSelectMultipleWithGroups, self).render(
                name=name, value=value, attrs=attrs, choices=choices
            ))
        return mark_safe(u'\n'.join(output))


class CategsForm(forms.Form):
    categs = forms.MultipleChoiceField(
        label='',
        widget=CheckboxSelectMultipleWithGroups(),
        choices=((t.name, t.name) for t in Tag.objects.all())
    )
