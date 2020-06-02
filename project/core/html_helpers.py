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

def create_options_list(items,
                        text_field,
                        value_field,
                        selected_value,
                        option_tag_attrs = {}):
    option_list = []

    if selected_value is None or selected_value == '':
        option_tag_attrs['value'] = ''
        option_tag_attrs['selected'] = 'selected'
        option_list.append(create_tag('option', **option_tag_attrs))
        option_list.append('Select...')
        option_list.append('</option>')

    for item in items:
        if str(item[value_field]) == str(selected_value):
            option_tag_attrs['selected'] = 'selected'
        else:
            option_tag_attrs.pop('selected', None)

        option_tag_attrs['value'] = str(item[value_field])

        option_list.append(create_tag('option', **option_tag_attrs))
        option_list.append(str(item[text_field]))
        option_list.append('</option>')

    return "".join(option_list)
