from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.views import View
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator

from .models import Rider
from .forms import RiderForm
from states.models import State
from states.repo import get_states_dict
from core import html_helpers
from core.stopwatch import StopWatch

import time
import urllib.parse

def convert_states_dict_to_options(states_dict, selected_state_id):
    select_markup = html_helpers.create_options_list(items = states_dict,
                                                     text_field = 'province',
                                                     value_field = 'id',
                                                     selected_value = selected_state_id,
                                                     option_tag_attrs = {})
    return select_markup

def get_states_options_list(request, selected_state_id):
    # rp:Todo: Consider using memcache later.
    sw = StopWatch('Time to load states list')
    sw.start()

    if 'states_dict' in request.session:
        print('fetched from session')
        states_dict = request.session['states_dict']
    else:
        states_dict = list(get_states_dict())
        request.session['states_dict'] = states_dict

    # states_dict = list(get_states_dict())

    result = convert_states_dict_to_options(states_dict, selected_state_id)
    sw.stop()
    sw.show_results()

    return result

class Edit(View):
    def get(self, request, id):
        '''
        Display an existing entity for editing.
        '''
        sw = StopWatch('Time to run rider.views.Edit method')
        sw.start()

        rider = Rider.objects.get(id=id)
        states_options_list = get_states_options_list(request, rider.state.id)

        form = RiderForm(request.POST or None, instance=rider)

        context =  {'form':form,
                    'rider_id' : id,
                    'states_options_list': states_options_list,
                    'form_action': reverse('update-rider', args=[id])
                    # 'form_action' : f'/riders/{id}'
                    }

        sw.stop()
        sw.show_results()

        return render(request, 'riders/show.html', context)

class Update(View):
    def post(self, request, id):
        '''
        Update an existing entity.
        '''
        rider_id = request.POST.get('id')
        state_id =  request.POST.get('state')
        if state_id == '':
            state_id = None
        states_options_list = get_states_options_list(request, state_id)

        rider = get_object_or_404(Rider, pk=id)
        form = RiderForm(request.POST or None, instance=rider)

        context =  {'form':form,
                    'rider_id' : id,
                    'states_options_list': states_options_list,
                    'form_action': reverse('update-rider', args=[id])
                    # 'form_action' : f'/riders/{id}'
                    }

        if form.is_valid():
            form.save()

            messages.info(request, f'{rider.full_name} updated.')

            route = reverse('riders-list')
            url = f'{route}?startswith={rider.last_name.lower()}'
            return redirect(url)
        else:
            return render(request, 'riders/show.html', context )

class New(View):
    def get(self, request):
        '''
        Display form for adding a new entity.
        '''
        states_options_list = get_states_options_list(request, None)

        rider = Rider()
        form = RiderForm(request.POST or None, instance=rider)

        context = {'form': form,
                   'rider_id': -1,
                   'states_options_list': states_options_list,
                   'form_action' : reverse_lazy('create-rider')}
        return render(request, 'riders/show.html', context)

class Delete(View):
    def post(self, request, id):
        rider = get_object_or_404(Rider, pk=id)
        rider.delete()

        messages.info(request, f'{rider.full_name} successfully deleted.')

        route = reverse('riders-list')
        url = f'{route}?startswith={rider.last_name.lower()}'

        return redirect(url)

class Index(View):
    PAGE_SIZE = 8

    def get_starts_with_results(self, request):
        startswith =  request.GET.get('startswith')
        riders = Rider.objects.filter(last_name__gte=startswith.lower()).order_by('last_name')

        if not riders:
            messages.info(request, f'Start-with search for "{startswith}" failed')

        return riders, None

    def get_search_results(self, request):
        search =  request.GET.get('search')
        riders = Rider.objects.filter(last_name__istartswith=search.upper()).order_by('last_name')

        if riders:
            messages.info(request, f'Search for "{search}" active')
        else:
            messages.info(request, f'Search for "{search}" failed')

        return riders, search

    def get_filtered_results(self, request):
        search = request.GET.get('search') or None
        startswith = request.GET.get('startswith') or None

        if search:
            return self.get_search_results(request)
        elif startswith:
            return self.get_starts_with_results(request)

        return None, None

    def get(self, request):
        '''
        Display the list of riders.
        '''

        sw = StopWatch('Fetch 200 riders')
        sw.start()

        riders, search = self.get_filtered_results(request)
        if riders is None:
            riders = Rider.objects.order_by('last_name')

        paginator = Paginator(riders, self.PAGE_SIZE)

        page_number = request.GET.get('page', 1)
        riders_page = paginator.get_page(page_number)

        context = {'riders': riders_page,
                   'search': search or '',
                   'msg_top': 0
                  }

        if 'deleted-msg' in request.session:
            messages.info(request,request.session['deleted-msg'])
            del request.session['deleted-msg']

        sw.stop()
        sw.show_results()
        if request.method == 'GET':
            return render(request, 'riders/index.html', context)

    def post(self, request):
        '''
        Add a new entity to database.
        '''
        state_id =  request.POST.get('state')
        states_options_list = get_states_options_list(request, state_id)

        rider = Rider()
        form = RiderForm(request.POST or None, instance=rider)

        context = {'form': form,
                   'rider_id': -1,
                   'states_options_list': states_options_list,
                   'form_action' : reverse_lazy('create-rider')}

        if form.is_valid():
            form.save()
            messages.info(request, f'{rider.full_name} successfully added.')

            route = reverse('riders-list')
            url = f'{route}?startswith={rider.last_name.lower()}'
            return redirect(url)

            # return redirect('riders-list')
        else:
            return render(request, 'riders/show.html', context)