import collections

from django import forms
from django.utils.safestring import mark_safe

from taggit.managers import TaggableManager
from taggit.models import Tag


class SelectTagField(forms.TypedMultipleChoiceField):
    widget = forms.CheckboxSelectMultiple


class CustomTaggableManager(TaggableManager):
    def __unicode__(self):
        return u"<%s:%s>" % (type(self), self.name)

    def formfield(self, form_class=SelectTagField, **kwargs):
        """
        Used when a model form is built. This determines what the
        form field should do
        """
        defaults = {
            'choices': ((t.name, t.name) for t in Tag.objects.all()),
        }
        defaults.update(kwargs)
        return super(CustomTaggableManager, self).formfield(
            form_class=form_class,
            **defaults
        )

    def value_from_object(self, instance):
        """
        Used when creating initial data for the form. We send all the tags,
        because their pks are put in the select widget
        """
        return getattr(instance, self.name).all()


class CheckboxSelectMultipleWithGroups(forms.CheckboxSelectMultiple):
    """
    Groups the choices based on their prefixes
    """
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
