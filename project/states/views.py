from django.shortcuts import render
from django.http import HttpResponse
from . models import State, Person
from core import html_helpers
from django.views import View
from . forms import PersonForm
from . dropdowns import get_states_dropdown

class Index(View):
    def get(self, request):
        form = PersonForm()

        ids = State.objects.get(abbreviation='IN').id
        x = st.province
        markup = get_states_dropdown()

        context = {
            'form': form,
            'states_options' : markup
        }
        return render(request,'states/index.html', context)
