from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, EventRegistration
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import *
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.models import User
from .utils import verify_token
from django.contrib import messages
from django.utils.timezone import now
from django.db.models import Count
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import EditProfileForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import ListView
from django.views.generic.edit import  CreateView, UpdateView, DeleteView
from django.http import HttpResponse
import csv
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse


"""Event Admin"""
class CreateEventView(LoginRequiredMixin,CreateView):
    model = Event
    form_class = EventForm
    template_name = 'create_event.html'
    success_url = reverse_lazy('admin_event_list')

class EditEventView(LoginRequiredMixin,UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'edit_event.html'
    success_url = reverse_lazy('admin_event_list')

class DeleteEventView(LoginRequiredMixin,DeleteView):
    model = Event
    template_name = 'delete_event_confirm.html'
    success_url = reverse_lazy('admin_event_list')

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_completed_events(request):
    Event.objects.filter(date__lt=timezone.now().date()).delete()
    return redirect('admin_event_list')

@login_required
@user_passes_test(lambda u: u.is_staff)
def download_participants(request, pk):
    event = get_object_or_404(Event, pk=pk)
    registrations = EventRegistration.objects.filter(event=event)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{event.name}_participants.csv"'

    writer = csv.writer(response)
    writer.writerow(['Username', 'Email', 'Phone Number', 'Department', 'Players'])

    for reg in registrations:
        # Safely extract player names (or any other info)
        players_str = ', '.join(player.get('name', '') for player in reg.players)

        writer.writerow([
            reg.user.username,
            reg.user.email,
            reg.phone_number,
            reg.get_department_display(),
            players_str
        ])

    return response

@login_required
@user_passes_test(lambda u: u.is_staff)
def download_volunteer_csv(request, event_id):
    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=401)

    event = get_object_or_404(Event, id=event_id)
    volunteers = VolunteerRegistration.objects.filter(event=event)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{event.name}_volunteers.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Roll Number', 'Department', 'Phone Number', 'Email', 'Registered At'])

    for v in volunteers:
        writer.writerow([
            v.name,
            v.rollnumber,
            v.get_department_display(),
            v.phone_number,
            v.user.email,
            v.created_at.strftime("%Y-%m-%d %H:%M:%S")
        ])

    return response

@login_required
@user_passes_test(lambda u: u.is_staff)
def contact_messages_view(request):
    contact_messages = ContactFormModel.objects.all().order_by('-created_at')
    return render(request, 'contact_messages.html', {'contact_messages': contact_messages})

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_contact_message(request, message_id):
    message = get_object_or_404(ContactFormModel, id=message_id)
    message.delete()
    messages.success(request, "Message deleted successfully.")
    return redirect('contact_messages')

# Restrict access to staff users only
class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

# List View
class AllowedEmailListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = AllowedEmail
    template_name = 'allowed_emails.html'
    context_object_name = 'emails'

# Create View
class AllowedEmailCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = AllowedEmail
    fields = ['email']
    template_name = 'allowed_email_form.html'
    success_url = reverse_lazy('allowed_email_list')

# Update View
class AllowedEmailUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = AllowedEmail
    fields = ['email']
    template_name = 'allowed_email_form.html'
    success_url = reverse_lazy('allowed_email_list')

# Delete View
class AllowedEmailDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = AllowedEmail
    template_name = 'allowed_email_confirm_delete.html'
    success_url = reverse_lazy('allowed_email_list')
    
@login_required
@user_passes_test(lambda u: u.is_staff)
def create_event_highlight(request):
    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        title = data.get('title')
        description = data.get('description')

        # Save the EventHighlight
        highlight = EventHighlight.objects.create(
            title=title,
            description=description
        )

        # Save associated images
        for image in images:
            EventImage.objects.create(
                event=highlight,
                image=image
            )

        return redirect('highlights_list')  # Replace with your actual redirect

    return render(request, 'create_highlight.html')  # Update path if needed

@login_required
@user_passes_test(lambda u: u.is_staff)
def volunteer_list_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    registrations = VolunteerRegistration.objects.filter(event=event)
    return render(request, 'volunteer_list.html', {
        'event': event,
        'registrations': registrations
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def event_participants(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    participants = EventRegistration.objects.filter(event=event)
    return render(request, 'event_participants.html', {'event': event, 'participants': participants})

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_participant(request, reg_id):
    registration = get_object_or_404(EventRegistration, id=reg_id)
    event_id = registration.event.id
    registration.delete()
    messages.success(request, "Participant deleted successfully.")
    return redirect('event_participants', event_id=event_id)

@user_passes_test(lambda u: u.is_staff)
def delete_volunteer(request, registration_id):
    registration = get_object_or_404(VolunteerRegistration, id=registration_id)
    event_id = registration.event.id
    if request.method == 'POST':
        registration.delete()
    return HttpResponseRedirect(reverse('volunteer_list_view', args=[event_id]))



@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_highlight(request, pk):
    if request.method == "POST" and request.user.is_staff:
        highlight = get_object_or_404(EventHighlight, pk=pk)
        highlight.delete()
    return redirect('highlights_list')  # change to your list view name

# Create your views here.

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_profile_view(request):
    return render(request, 'admin_profile.html')

@login_required
def profile_view(request):
    registered_events = EventRegistration.objects.filter(user=request.user).select_related('event')
    volunteered_events = VolunteerRegistration.objects.filter(user=request.user).select_related('event')

    return render(request, 'profile.html', {
        'registered_events': registered_events,
        'volunteered_events': volunteered_events,
    })
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})



@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully!")
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})



@login_required
def event_list(request):
    if request.user.is_superuser:
        return redirect('admin_event_list')
    query = request.GET.get('q', '')  
    events = Event.objects.all().order_by('-created_at')

    
    registered_event_ids = []
    if request.user.is_authenticated:
        registered_event_ids = EventRegistration.objects.filter(user=request.user).values_list('event_id', flat=True)

    if query:
        searched_events = events.filter(name__icontains=query)
        return render(request, 'event_list.html', {'events':searched_events , 'query':query, 'registered_event_ids': registered_event_ids})

    sports_events = Event.objects.filter(category='Sports').order_by('-created_at')
    cultural_events = Event.objects.filter(category='Cultural').order_by('-created_at')
    coding_events = Event.objects.filter(category='Coding').order_by('-created_at')
    other_events = Event.objects.filter(category='Other').order_by('-created_at') 

    return render(request, 'event_list.html', {
        'sports_events': sports_events,
        'coding_events': coding_events,
        'cultural_events': cultural_events,
        'other_events': other_events,
        'registered_event_ids': registered_event_ids,
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_event_list(request):
    query = request.GET.get('q', '')  
    events = Event.objects.all().order_by('-created_at')

    registered_event_ids = []
    if request.user.is_authenticated:
        registered_event_ids = EventRegistration.objects.filter(user=request.user).values_list('event_id', flat=True)

    if query:
        searched_events = events.filter(name__icontains=query)
        return render(request, 'admin_event_list.html', {
            'events': searched_events,
            'query': query,
            'registered_event_ids': registered_event_ids
        })

    sports_events = Event.objects.filter(category='Sports').order_by('-created_at')
    cultural_events = Event.objects.filter(category='Cultural').order_by('-created_at')
    coding_events = Event.objects.filter(category='Coding').order_by('-created_at')
    other_events = Event.objects.filter(category='Other').order_by('-created_at') 

    return render(request, 'admin_event_list.html', {
        'sports_events': sports_events,
        'coding_events': coding_events,
        'cultural_events': cultural_events,
        'other_events': other_events,
        'registered_event_ids': registered_event_ids
    })

@login_required
def registered_events(request):
    registrations = EventRegistration.objects.filter(user=request.user)
    registered_events = [registration.event for registration in registrations]
    return render(request, 'registered_events.html', {'registered_events': registered_events})

@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    is_registered = EventRegistration.objects.filter(user=request.user, event=event).exists()
    is_volunteered = VolunteerRegistration.objects.filter(user=request.user, event=event).exists()
    return render(request, 'event_desc.html', {'event': event, 'is_registered': is_registered, 'is_volunteered': is_volunteered})

@login_required
def event_registration(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    
    if EventRegistration.objects.filter(user=request.user, event=event).exists():
        return render(request, 'already_registered.html', {'event': event})

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

            registration = EventRegistration.objects.create(
                user=request.user,
                event=event,
                phone_number=form.cleaned_data['phone_number'],
                department=form.cleaned_data['department'],
                players=players
            )

           
            send_mail(
                subject=f"Registration Successful: {event.name}",
                message=f"Dear {request.user.username},\n\n"
                        f"You have successfully registered for the event '{event.name}' scheduled on {event.date} at {event.venue}.\n"
                        f"Thank you for participating!\n\n"
                        f"Best Regards,\nEvent Team",
                from_email='nihalpatel7864@gmail.com',
                recipient_list=[request.user.email],
                fail_silently=False,
            )

            return redirect('event_list')
    else:
        form = EventRegistrationForm(event=event)

    return render(request, 'event_registration.html', {'form': form, 'event': event})
    
@login_required
def unregister_event(request, reg_id):
    registration = get_object_or_404(EventRegistration, id=reg_id, user=request.user)
    if request.method == 'POST':
        registration.delete()
        return redirect('profile') 
    return render(request, 'confirm_unregister.html', {'event': registration.event, 'type': 'event'})
    
@login_required
def unregister_volunteer(request, reg_id):
    registration = get_object_or_404(VolunteerRegistration, id=reg_id, user=request.user)
    if request.method == 'POST':
        registration.delete()
        return redirect('profile')
    return render(request, 'confirm_unregister.html', {'event': registration.event, 'type': 'volunteer'})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  
            user.save()

           
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            verification_link = f"http://{current_site.domain}/verify/{uid}/{token}/"

            
            subject = "Verify Your Email Address"
            message = render_to_string('registration/verification_email.html', {
                'user': user,
                'verification_link': verification_link,
            })
            send_mail(subject, message, 'your-email@gmail.com', [user.email])

            return render(request, 'registration/verification_sent.html')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    if user and user.is_active == False and verify_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'registration/verification_success.html')
    else:
        return render(request, 'registration/verification_failed.html')
    
@login_required
def contactform(request):
    form  = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_request = form.save(commit=False)
            contact_request.user = request.user
            contact_request.save()
            messages.success(request,'Your message has been submitted successfully')
            return redirect('contact')
            
    return render(request, 'contact_form.html',{'form':form})

@login_required
def volunteer_events(request):
    events = Event.objects.filter(volunteer_requirement__gt=0).annotate(volunteer_count=Count('volunteerregistration'))

    registered_event_ids = EventRegistration.objects.filter(user=request.user).values_list('event_id', flat=True)

    volunteer_registered_event_ids = VolunteerRegistration.objects.filter(user=request.user).values_list('event_id', flat=True)

    return render(request, 'volunteer_events.html', {
        'events': events,
        'registered_event_ids': registered_event_ids, 
        'volunteer_registered_event_ids': volunteer_registered_event_ids,  
    })


@login_required
def volunteer_registration(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    registered_volunteers = VolunteerRegistration.objects.filter(event=event).count()


    if registered_volunteers >= event.volunteer_requirement:
        messages.error(request, "Volunteer slots for this event are full.")
        return redirect('volunteer_events')


    if VolunteerRegistration.objects.filter(user=request.user, event=event).exists():
        messages.warning(request, "You have already registered as a volunteer for this event.")
        return redirect('volunteer_events')


    if EventRegistration.objects.filter(user=request.user, event=event).exists():
        messages.error(request, "You cannot register as a volunteer because you are already a participant.")
        return redirect('volunteer_events')


    if request.method == 'POST':
        form = VolunteerRegistrationForm(request.POST)
        if form.is_valid():
            volunteer = form.save(commit=False)
            volunteer.user = request.user
            volunteer.event = event
            volunteer.save()
            messages.success(request, "You have successfully registered as a volunteer.")
            return redirect('volunteer_events')
    else:
        form = VolunteerRegistrationForm()

    return render(request, 'volunteer_registration.html', {'form': form, 'event': event})

@login_required
def highlights_list(request):
    highlights = EventHighlight.objects.all().order_by('-created_at')
    return render(request, 'highlights_list.html', {'highlights': highlights})

@login_required
def highlight_detail(request, pk):
    highlight = get_object_or_404(EventHighlight, pk=pk)
    return render(request, 'highlights_detail.html', {'highlight': highlight})