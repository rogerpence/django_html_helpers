from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import View
from .models import Rider
from .forms import RiderForm
from states.models import State
from core import repo

def get_states_options_list(selected_state_abbreviation):
    states_list = (State.objects
                        .all()
                        .order_by('province')
                        .values('id', 'province', 'abbreviation'))
    select_markup = repo.create_options_list(items = states_list,
                                             text_field = 'province',
                                             value_field = 'id',
                                             selected_value_field_name = 'abbreviation',
                                             selected_value_field_value = selected_state_abbreviation,
                                             option_tag_attrs = {})

    return select_markup

class Show(View):
    def get(self, request, id):
        rider = Rider.objects.get(id=id)
        options_list = get_states_options_list(rider.state.abbreviation)
        form = RiderForm(request.POST or None, instance=rider)

        context = {'form': form, 'rider_id': id, 'options_list': options_list }
        return render(request, 'rider/index.html', context)

class Store(View):
    def post(self, request):
        id = request.POST.get('id')
        state =  request.POST.get('state')
        rider = get_object_or_404(Rider, pk=id)

        full_name = rider.full_name
        form = RiderForm(request.POST or None, instance=rider)
        options_list = get_states_options_list(form.cleaned_data.get('state').abbreviation)

        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            return render(request, 'rider/index.html', {'form':form, 'rider_id' : id, 'options_list': options_list})

class Index(View):
    def get(self, request):
        rider = Rider.objects.get(id=1)

        context = {'form':rider}
        if request.method == 'GET':
            return render(request, 'rider/index.html', context)
