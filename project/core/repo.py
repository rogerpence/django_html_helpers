def create_tag(tagName, **kwargs):
    attributes = []
    attributes_string = ''
    space = ' '

    # if type(kwargs) is dict and kwargs is not None:
    if kwargs is not None:
        for key, value in kwargs.items():
            attributes.append(f'{key}="{value}"')
    if (len(attributes) > 0):
        return f'<{tagName} {space.join(attributes)}>'
    else:
        return f'<{tagName}>'

def create_select_tag(items,
                      text_field,
                      value_field,
                      current_value,
                      select_tag_attrs = {},
                      option_tag_attrs = {}):
    select_markup = []

    select_markup.append(create_tag('select',**select_tag_attrs))

    for item in items:
        if item[value_field] == current_value:
            option_tag_attrs['selected'] = 'selected'
        else:
            option_tag_attrs.pop('selected', None)

        option_tag_attrs['value'] = item[value_field]

        select_markup.append(create_tag('option', **option_tag_attrs))
        select_markup.append(item[text_field])
        select_markup.append('</option>')

    select_markup.append('</select>')

    return "".join(select_markup)
