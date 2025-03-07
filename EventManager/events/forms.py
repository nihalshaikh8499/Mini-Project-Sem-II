from django import forms 
from .models import Event,EventRegistration
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

class EventRegistrationForm(forms.ModelForm):
    DEPARTMENT_CHOICES = [
        ('FY MCA', 'First Year MCA'),
        ('SY MCA', 'Second Year MCA'),
        ('FY MBA', 'First Year MBA'),
        ('SY MBA', 'Second Year MBA'),
    ]

    phone_number = forms.CharField(max_length=15, label="Phone Number")
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')  
        super().__init__(*args, **kwargs)

        for i in range(1, event.max_players + 1):
            self.fields[f'player_{i}_name'] = forms.CharField(
                required=i <= event.min_players,
                label=f'Player {i} Name'
            )
            self.fields[f'player_{i}_roll'] = forms.CharField(
                required=i <= event.min_players,
                label=f'Player {i} Roll Number'
            )

    class Meta:
        model = EventRegistration
        fields = ['phone_number', 'department']