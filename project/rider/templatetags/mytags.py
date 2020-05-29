from django import template

register = template.Library()

@register.filter(name='rptest')
def rptest(value, arg):
    # print(value)
    # x = arg
    # return value
    # value['class'] = 'bob'
    print(value.name)
    # print(value.field.value)
    # print(value.form.data)

    print(value.__dict__.keys())
    return value

# This is what a field is passed to a filter.
# django.forms.boundfield.BoundField

# from django import template

# register = template.Library()

# @register.filter
# def index(indexable, i):
#     return indexable[i]