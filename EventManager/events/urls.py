from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name = 'event_list'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('<int:event_id>/register/', views.event_registration, name='event_registration'),
    path('register/', views.register, name='register'),

]