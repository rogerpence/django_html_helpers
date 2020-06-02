from django import forms
from .models import Person, State

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'state')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['state'].queryset = (State.objects
                                         .all()
                                         .order_by('province'))

