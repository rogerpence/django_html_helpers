"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rider.views import index as RiderIndex
from rider.views import new as RiderNew
from rider.views import edit as RiderEdit
from rider.views import delete as RiderDelete
from rider.views import update as RiderUpdate

from states.views import Index as StatesIndex

urlpatterns = [
    path('admin/', admin.site.urls),

    path('states/', StatesIndex.as_view(), name='states' ),


    path('riders/<int:id>/edit/', RiderEdit),
    path('riders/<int:id>/delete/', RiderDelete),
    path('riders/<int:id>/', RiderUpdate, name='update-rider'),
    path('riders/new/', RiderNew, name='new-rider'),
    path('riders/', RiderIndex, name='riders-list'),
    path('riders/', RiderIndex, name="create-rider"),

    path('', RiderIndex),

]
