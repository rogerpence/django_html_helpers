from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.views import View
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods

from .models import Rider
from .forms import RiderForm
from states.models import State
from states.repo import get_states_dict
from core import html_helpers
from core.stopwatch import StopWatch
from core.dropdowns import get_states_dropdown_list

import time
import urllib.parse

@require_http_methods(["GET"])
def edit(request, id):
    '''
    Display an existing entity for editing.
    '''
    rider = Rider.objects.get(id=id)
    states_options_list = get_states_dropdown_list(rider.state.id)

    form = RiderForm(request.POST or None, instance=rider)

    context =  {'form':form,
                'rider_id' : id,
                'states_options_list': states_options_list,
                'form_action': reverse('update-rider', args=[id])
                }

    return render(request, 'riders/show.html', context)

@require_http_methods(["POST"])
def update(request, id):
    '''
    Update an existing entity.
    '''
    rider_id = request.POST.get('id')
    state_id =  request.POST.get('state')

    states_options_list = get_states_dropdown_list(state_id)

    rider = get_object_or_404(Rider, pk=id)
    form = RiderForm(request.POST or None, instance=rider)

    context =  {'form':form,
                'rider_id' : id,
                'states_options_list': states_options_list,
                'form_action': reverse('update-rider', args=[id])
                }

    if form.is_valid():
        form.save()

        messages.info(request, f'{rider.full_name} updated.')

        route = reverse('riders-list')
        url = f'{route}?startswith={rider.last_name.lower()}'
        return redirect(url)
    else:
        return render(request, 'riders/show.html', context )

@require_http_methods(["GET"])
def new(request):
    '''
    Display form for adding a new entity.
    '''
    states_options_list = get_states_dropdown_list()

    rider = Rider()
    form = RiderForm(request.POST or None, instance=rider)

    context = {'form': form,
                'rider_id': -1,
                'states_options_list': states_options_list,
                'form_action' : reverse_lazy('create-rider')}
    return render(request, 'riders/show.html', context)

@require_http_methods(["POST"])
def delete(request, id):
    rider = get_object_or_404(Rider, pk=id)
    rider.delete()

    messages.info(request, f'{rider.full_name} successfully deleted.')

    route = reverse('riders-list')
    url = f'{route}?startswith={rider.last_name.lower()}'

    return redirect(url)

@require_http_methods(["GET", "POST"])
def index(request):
    if request.method == 'GET':
        return index_get(request)

    elif request.method == 'POST':
        return index_post(request)

@require_http_methods(["GET"])
def index_get(request):
    '''
    Display the list of riders.
    '''
    PAGE_SIZE = 8

    riders, search = get_filtered_results(request)
    if riders is None:
        riders = Rider.objects.order_by('last_name')

    paginator = Paginator(riders, PAGE_SIZE)

    page_number = request.GET.get('page', 1)
    riders_page = paginator.get_page(page_number)

    context = {'riders': riders_page,
                'search': search or '',
                'msg_top': 0
                }

    if 'deleted-msg' in request.session:
        messages.info(request,request.session['deleted-msg'])
        del request.session['deleted-msg']

    if request.method == 'GET':
        return render(request, 'riders/index.html', context)

@require_http_methods(["POST"])
def index_post(request):
    '''
    Add a new entity to database.
    '''
    state_id =  request.POST.get('state')
    states_options_list = get_states_dropdown_list(state_id)

    rider = Rider()
    form = RiderForm(request.POST or None, instance=rider)

    context = {'form': form,
                'rider_id': -1,
                'states_options_list': states_options_list,
                'form_action' : reverse('create-rider')}

    if form.is_valid():
        form.save()
        messages.info(request, f'{rider.full_name} successfully added.')

        route = reverse('riders-list')
        url = f'{route}?startswith={rider.last_name.lower()}'
        return redirect(url)

    else:
        return render(request, 'riders/show.html', context)

# -----------------------------------------------------------------------------
# Helper functions.
# -----------------------------------------------------------------------------

def get_starts_with_results(request):
    '''
    Get rider list where 'last_name' is greater than or equal to 'startswith' value.
    '''
    startswith =  request.GET.get('startswith')
    riders = Rider.objects.filter(last_name__gte=startswith.lower()).order_by('last_name')

    if not riders:
        messages.info(request, f'Start-with search for "{startswith}" failed')

    return riders, startswith

def get_search_results(request):
    '''
    Get rider list where 'last_name' starts with 'search' value.
    '''
    search =  request.GET.get('search')
    riders = Rider.objects.filter(last_name__istartswith=search.upper()).order_by('last_name')

    if riders:
        messages.info(request, f'Search for "{search}" active')
    else:
        messages.info(request, f'Search for "{search}" failed')

    return riders, search

def get_filtered_results(request):
    '''
    Dispatch filtered queries for rider list.
    '''
    search = request.GET.get('search') or None
    startswith = request.GET.get('startswith') or None

    if search:
        return get_search_results(request)
    elif startswith:
        return get_starts_with_results(request)

    return None, None