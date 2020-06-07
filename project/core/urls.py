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

from rider.views import Index as RiderIndex
from rider.views import New as RiderNew
# from rider.views import Create as RiderCreate
from rider.views import Edit as RiderEdit
from rider.views import Delete as RiderDelete
from rider.views import Update as RiderUpdate

from states.views import Index as StatesIndex

urlpatterns = [
    # path('', include('states.urls'), name="index"),
    # path('', include('states.urls'), name="index"),
    path('admin/', admin.site.urls),

    # !! no URLs are necessary in the app.
    path('states/', StatesIndex.as_view(), name='states' ),

    path('riders/', RiderIndex.as_view(), name='riders-list'),
    path('riders/', RiderIndex.as_view(), name="create-rider"),

    path('riders/<int:id>/edit/', RiderEdit.as_view()),
    path('riders/<int:id>/delete/', RiderDelete.as_view()),
    path('riders/<int:id>/', RiderUpdate.as_view(), name='update-rider'),
    path('riders/new/', RiderNew.as_view(), name='new-rider'),

    # path('riders/show.html')




    path('', RiderIndex.as_view()),


]
