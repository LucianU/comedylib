import collections

from django import forms
from django.core.cache import cache
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

        # We want to display the categories in the groups that they
        # are a part of:
        # group
        #   category
        #   category
        # Now, we need to generate all choices with a single call to
        # the `render` of the base class to avoid ID duplication. Then
        # we need to insert at the right location the groups themselves
        # between the choices.

        # We start with index 1 to take into account the <ul> starting tag
        index = 1
        indexed_groups = {}
        formatted_choices = []

        for group, group_choices in groups.iteritems():
            indexed_groups[index] = u'<h3>%s</h3>' % group
            formatted_choices.extend(group_choices)
            # We extend the index by the group and all its choices
            index += (1 + len(group_choices))

        # We replace the initial choices, because they don't have the
        # group and category separate. There, they are in the format
        # group:category
        self.choices = formatted_choices

        # We split the output to have a list which we can modify
        output = super(CheckboxSelectMultipleWithGroups, self).render(
            name=name, value=value, attrs=attrs, choices=choices
        ).split('\n')

        # We insert the groups between the categories
        for index, group in indexed_groups.iteritems():
            output[index:index] = [group]

        return mark_safe(u'\n'.join(output))


class CategsForm(forms.Form):
    categs = forms.MultipleChoiceField(
        label='',
        widget=CheckboxSelectMultipleWithGroups(),
        choices=()
    )

    def __init__(self, role, *args, **kwargs):
        super(CategsForm, self).__init__(*args, **kwargs)

        cache_key = 'tag_choices_role_%s' % role
        tag_choices = cache.get(cache_key)
        if tag_choices is None:
            tags = Tag.objects.filter(
                taggit_taggeditem_items__collection__role=role
            ).distinct()
            tag_choices = [(t.name, t.name) for t in tags]
            # Cache for 24 hours
            cache.set(cache_key, tag_choices, 60 * 60 * 24)

        self.fields['categs'].choices = tag_choices
