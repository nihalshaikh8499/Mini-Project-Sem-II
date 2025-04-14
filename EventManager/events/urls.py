from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import *




urlpatterns = [
    path('', views.event_list, name = 'event_list'),
    path('admin_panel/events/', views.admin_event_list, name='admin_event_list'),
    path('contact-messages/', views.contact_messages_view, name='contact_messages'),
    path('delete-contact-message/<int:message_id>/', views.delete_contact_message, name='delete_contact_message'),

    path('event/<int:pk>/edit/', EditEventView.as_view(), name='edit_event'),
    path('event/<int:pk>/delete/', DeleteEventView.as_view(), name='delete_event'),
    path('event/<int:pk>/download/', download_participants, name='download_participants'),
    path('event/create/', CreateEventView.as_view(), name='create_event'),
    path('event/delete_completed/', delete_completed_events, name='delete_completed_events'),

    path('event/<int:event_id>/participants/', views.event_participants, name='event_participants'),
    path('delete-participant/<int:reg_id>/', views.delete_participant, name='delete_participant'),
    

    path('allowed-emails/', AllowedEmailListView.as_view(), name='allowed_email_list'),
    path('allowed-emails/add/', AllowedEmailCreateView.as_view(), name='allowed_email_add'),
    path('allowed-emails/edit/<int:pk>/', AllowedEmailUpdateView.as_view(), name='allowed_email_update'),
    path('allowed-emails/delete/<int:pk>/', AllowedEmailDeleteView.as_view(), name='allowed_email_delete'),

    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('<int:event_id>/register/', views.event_registration, name='event_registration'),
    path('registered_events/', views.registered_events, name='registered_events'),
    path('contact_form/', views.contactform, name='contact'),

    path('register/', register, name='register'),
    path('verify/<str:uidb64>/<str:token>/', verify_email, name='verify_email'),

   
    path('admin_profile/', views.admin_profile_view, name='admin_profile'),
    path('profile/', views.profile_view, name='profile'),
    path('unregister/event/<int:reg_id>/', views.unregister_event, name='unregister_event'),
    path('unregister/volunteer/<int:reg_id>/', views.unregister_volunteer, name='unregister_volunteer'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),

    path('register/', views.register, name='register'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('volunteer-events/', views.volunteer_events, name='volunteer_events'),
    path('event/<int:event_id>/volunteers/', views.volunteer_list_view, name='volunteer_list_view'),
    path('volunteer/delete/<int:registration_id>/', views.delete_volunteer, name='delete_volunteer'),
    path('<int:event_id>/volunteer/', views.volunteer_registration, name='volunteer_registration'),
    path('events/<int:event_id>/download_volunteers/', views.download_volunteer_csv, name='download_volunteer_csv'),

   
    path('highlights/', views.highlights_list, name='highlights_list'),
    path('highlights/create/', views.create_event_highlight, name='create_highlight'),
    path('highlight/delete/<int:pk>/', views.delete_highlight, name='delete_highlight'),
    path('highlights/<int:pk>/', views.highlight_detail, name='highlight_detail'),
]