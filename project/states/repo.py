from .models import State

def get_states_dict():
    states_dict = (State.objects
                        .all()
                        .order_by('province')
                        .values('id', 'province', 'abbreviation'))
    return states_dict