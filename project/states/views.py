from django.shortcuts import render
from django.http import HttpResponse
from . models import State
from core import repo

def index(request):
    option_tag_attrs = {}
    # States_list needs to be a dictionary--note use of values() in the
    # to ensure that.
    states_list = (State.objects
                        .all()
                        .order_by('province')
                        .values('id', 'province', 'abbreviation'))



    select_markup = repo.create_options_list(items = states_list,
                                             text_field = 'province',
                                             value_field = 'id',
                                             selected_value = '18',
                                             option_tag_attrs = option_tag_attrs)

    context = {
        "select_states": select_markup,
    }

    return render(request,'states/index.html', context)
