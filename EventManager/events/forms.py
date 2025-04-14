from django import forms 
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.widgets import FileInput




class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username','email','password1','password2')
    def clean_email(self):
        email = self.cleaned_data.get('email')
    
        if not AllowedEmail.objects.filter(email=email).exists():
            raise ValidationError("This email is not allowed to register.")
        return email


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'name', 'description', 'category', 'date', 'time', 'venue',
            'image', 'min_players', 'max_players', 'rule_book',
            'volunteer_requirement', 'registration_deadline'
        ]

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'registration_deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']



class EventRegistrationForm(forms.ModelForm):
    DEPARTMENT_CHOICES = [
        ('FY MCA', 'First Year MCA'),
        ('SY MCA', 'Second Year MCA'),
        ('FY MBA', 'First Year MBA'),
        ('SY MBA', 'Second Year MBA'),
    ]

    phone_number = forms.CharField(max_length=10, label="Phone Number")
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

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactFormModel
        fields = ('subject','message')
    
class VolunteerRegistrationForm(forms.ModelForm):
    DEPARTMENT_CHOICES = [
        ('FY MCA', 'First Year MCA'),
        ('SY MCA', 'Second Year MCA'),
        ('FY MBA', 'First Year MBA'),
        ('SY MBA', 'Second Year MBA'),
    ]

    phone_number = forms.CharField(max_length=10, label="Phone Number")
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = VolunteerRegistration
        fields = ['name', 'rollnumber', 'phone_number', 'department']


    