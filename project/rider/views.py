from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import View
from .models import Rider
from .forms import RiderForm

class Show(View):
    def get(self, request, id):
        rider = Rider.objects.get(id=id)
        form = RiderForm(request.POST or None, instance=rider)

        context = {'form': form, 'rider_id': id}
        return render(request, 'rider/index.html', context)

class Store(View):
    def post(self, request):
        id = request.POST.get('id')
        rider = get_object_or_404(Rider, pk=id)

        full_name = rider.full_name
        form = RiderForm(request.POST or None, instance=rider)

        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            return render(request, 'rider/index.html', {'form':form, 'rider_id' : id})

class Index(View):
    def get(self, request):
        rider = Rider.objects.get(id=1)

        context = {'form':rider}
        if request.method == 'GET':
            return render(request, 'rider/index.html', context)
