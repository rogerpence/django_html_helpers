from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.views import View
import urllib.parse
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from .models import Rider
from .forms import RiderForm
from states.models import State
from states.repo import get_states_dict
# from core import repo
from core import html_helpers
from core.stopwatch import StopWatch
import time

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
            return redirect('riders_list')
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

# class Create(View):
#     def post(self, request):
#         '''
#         Add a new entity to database.
#         '''
#         state_id =  request.POST.get('state')
#         states_options_list = get_states_options_list(request, state_id)

#         rider = Rider()
#         form = RiderForm(request.POST or None, instance=rider)

#         context = {'form': form,
#                    'rider_id': -1,
#                    'states_options_list': states_options_list,
#                    'form_action' : reverse_lazy('create-rider')}

#         if form.is_valid():
#             form.save()
#             return redirect('riders_list')
#         else:
#             return render(request, 'riders/show.html', context)

class Delete(View):
    def post(self, request, id):
        rider = get_object_or_404(Rider, pk=id)
        rider.delete()
        route = reverse('riders_list')
        msg = urllib.parse.quote(f'{rider.full_name} successfully deleted.')
        url = f'{route}?flash={msg}'
        return redirect(url)

class Index(View):
    PAGE_SIZE = 8

    def get(self, request):
        '''
        Display the list of riders.
        '''

        if 'search' in request.GET:
            search =  request.GET.get('search')
            print(search.upper())
        else:
            search = None

        msg = request.GET.get('flash') or None

        sw = StopWatch('Fetch 200 riders')
        sw.start()

        if search:
            riders = Rider.objects.filter(last_name__istartswith=search.upper()).order_by('last_name')

        if (search and len(riders) == 0):
            msg = f'Search for "{search}" failed'
            search = None

        if (search and len(riders) == 0) or not search:
            riders = Rider.objects.order_by('last_name')

        paginator = Paginator(riders, self.PAGE_SIZE)

        page_number = request.GET.get('page', 1)
        riders_page = paginator.get_page(page_number)

        context = {'riders': riders_page,
                   'search': search if search is not None else '',
                   'flash': msg
                  }

        sw.stop()
        sw.show_results()
        if request.method == 'GET':
            messages.add_message(request, messages.INFO, 'Hello world.')
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
            return redirect('riders_list')
        else:
            return render(request, 'riders/show.html', context)
