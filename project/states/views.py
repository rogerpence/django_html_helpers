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
    states_list = State.objects.all().order_by('province').values()
    select_markup = repo.create_select_tag(states_list,
                                           'province',
                                           'abbreviation',
                                           current_state,
                                           select_tag_attrs,
                                           option_tag_attrs)


    # current_state = 'IN'
    # select_markup = []
    # states_list = State.objects.all().order_by('province')

    # select_markup.append(repo.create_tag('select', **{
    #     'id' : 'state',
    #     'name': 'state',
    #     'class': 'm-32 px-4 center',
    # }))

    # for state in states_list:
    #     print(type(state))
    #     if state.abbreviation == current_state:
    #         select_markup.append(repo.create_tag('option', **{
    #                                              'value' : state.abbreviation,
    #                                              'selected': 'selected'
    #                                             }))
    #     else:
    #         select_markup.append(repo.create_tag('option', **{
    #                                              'value' : state.abbreviation,
    #                                             }))
    #     select_markup.append(state.province)
    #     select_markup.append('</option>')

    # select_markup.append('</select>')

    context = {
        "states" : states_list,
        "select_states": select_markup,
    }

    return render(request,'states/index.html', context)

    # return HttpResponse("Hello, world. You're at the states index.")