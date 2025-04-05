from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import register, verify_email



urlpatterns = [
    path('', views.event_list, name = 'event_list'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('<int:event_id>/register/', views.event_registration, name='event_registration'),
    path('registered_events/', views.registered_events, name='registered_events'),
    path('contact_form/', views.contactform, name='contact'),

    path('register/', register, name='register'),
    path('verify/<str:uidb64>/<str:token>/', verify_email, name='verify_email'),

    path('register/', views.register, name='register'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('volunteer-events/', views.volunteer_events, name='volunteer_events'),
    path('<int:event_id>/volunteer/', views.volunteer_registration, name='volunteer_registration'),

    path('highlights/', views.highlights_list, name='highlights_list'),
    path('highlights/<int:pk>/', views.highlight_detail, name='highlight_detail'),
]