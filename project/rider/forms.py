from django import forms
from .models import Rider

class RiderForm(forms.ModelForm):
    class Meta:
        model = Rider
        # fields = '__all__'
        fields = ['first_name', 'last_name', 'address', 'city', 'phone', 'state']

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')
        if data == 'roger':
            raise forms.ValidationError('You cannot be roger')
        return data

    # def clean_state(self):
    #     data = self.cleaned_data.get('first_name')
    #     if data == '*None':
    #         raise forms.ValidationError('Please select a state')
    #     return data
