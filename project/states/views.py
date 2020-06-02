from django.shortcuts import render
from django.http import HttpResponse
from . models import State, Person
from core import html_helpers
from django.views import View
from . forms import PersonForm

class Index(View):
    def get(self, request):
        form = PersonForm()

        context = {
            'form': form
        }
        return render(request,'states/index.html', context)
