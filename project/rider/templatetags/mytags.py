from django import template

register = template.Library()

@register.simple_tag
def page_search_qs(page, increment, search):
    ''' Create a query string
        if search is falsy:
            ?page=n
        else
            ?page=n&search=s
    '''
    if search:
        search_qs =  f'&search={search}'
    else:
        search_qs = ''

    return f'?page={max([page + increment, 1])}{search_qs}'

@register.filter(name='search')
def rptest(value):
    if value:
        return f'&search={value}'
    else:
        return ''
    # print(value)
    # x = arg
    # return value
    # value['class'] = 'bob'
    print(value.name)
    # print(value.field.value)
    # print(value.form.data)

    print(value.__dict__.keys())
    return value


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