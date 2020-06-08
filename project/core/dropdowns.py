from states.models import State
from . import html_helpers

def get_states_dropdown_list(selected_state_id=None):
    if selected_state_id == '':
        selected_state_id = None

    states_dict = (State.objects
                            .all()
                            .order_by('province')
                            .values('id', 'province'))

    select_markup = html_helpers.create_options_list(items = states_dict,
                                                     text_field = 'province',
                                                     value_field = 'id',
                                                     selected_value = selected_state_id)

    return select_markup
