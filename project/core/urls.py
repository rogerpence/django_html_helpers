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

#   Route name   URL                  Verb          Description
#   --------------------------------------------------------------
#   Index        /riders              GET           Display a list of riders
#   New          /riders/new          GET           Display a form for new rider
#   Create       /riders              POST          Add a new rider to DB
#   Show         /riders/:id          GET           Show a rider
#   Edit         /riders/:id/edit     GET           Show a rider for editing
#   Update       /riders/:id          PUT/POST      Update a rider to DB
#   Destroy      /riders/:id          DELETE/POST   Delete a rider
#   Destroy      /riders/:id/delete   DELETE/POST   Delete a rider