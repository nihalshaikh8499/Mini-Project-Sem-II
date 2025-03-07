from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, EventRegistration
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import UserRegistrationForm, EventRegistrationForm
# Create your views here.

# def index(request):
#     return render(request, 'index.html')

@login_required
def event_list(request):
    events = Event.objects.all().order_by('-created_at') 

    return render(request, 'event_list.html', {'events':events})

@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_desc.html', {'event':event})

def event_registration(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = EventRegistrationForm(request.POST, event=event)
        if form.is_valid():
            players = [
                {
                    'name': form.cleaned_data[f'player_{i}_name'],
                    'roll_number': form.cleaned_data[f'player_{i}_roll']
                }
                for i in range(1, event.max_players + 1)
                if f'player_{i}_name' in form.cleaned_data and f'player_{i}_roll' in form.cleaned_data
            ]

            EventRegistration.objects.create(
                event=event,
                phone_number=form.cleaned_data['phone_number'],
                department=form.cleaned_data['department'],
                players=players
            )
            return redirect('event_list')  

    else:
        form = EventRegistrationForm(event=event)

    return render(request, 'event_registration.html', {'form': form, 'event': event})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('event_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form':form})
