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

def get_options_list(items_list, value_key, text_key, selected_value):
    options_list = []

    for item in items_list:
        if str(item[value_key]) == str(selected_value):
            selected = ' selected=selected'
        else:
            selected = ''
        options_list.append(f'<options value="{str(item[value_key])}{selected}">{item[str(text_key)]}</options>')
    return "".join(options_list)

def create_options_list(items,
                        text_field,
                        value_field,
                        selected_value,
                        option_tag_attrs = {}):
    option_list = []

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
