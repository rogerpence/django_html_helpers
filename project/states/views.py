from django.shortcuts import render
from django.http import HttpResponse
from . models import State
from core import repo

def index(request):
    current_state = 'IN'
    select_tag_attrs = {
        'id' : 'state',
        'name': 'state',
        'class': 'm-32 px-4 center',
    }
    option_tag_attrs = {}
    # States_list needs to be a dictionary--note use of values() in the
    # to ensure that.
    states_list = State.objects.all().order_by('province').values()
    select_markup = repo.create_select_tag(states_list,
                                           'province',
                                           'abbreviation',
                                           current_state,
                                           select_tag_attrs,
                                           option_tag_attrs)

    context = {
        "select_states": select_markup,
    }

    return render(request,'states/index.html', context)
