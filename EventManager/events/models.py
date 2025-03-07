from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Event(models.Model):
    EVENT_CATEGORIES = [
        ('Coding', 'Coding Competition'),
        ('Sports', 'Sports Event'),
        ('Cultural', 'Cultural Event'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EVENT_CATEGORIES)
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=255)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)  
    min_players = models.PositiveIntegerField(default=1)  
    max_players = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class EventRegistration(models.Model):
    DEPARTMENT_CHOICES = [
        ('FY MCA', 'First Year MCA'),
        ('SY MCA', 'Second Year MCA'),
        ('FY MBA', 'First Year MBA'),
        ('SY MBA', 'Second Year MBA'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)  
    department = models.CharField(max_length=10, choices=DEPARTMENT_CHOICES)  
    players = models.JSONField()  

    def __str__(self):
        return f"Registration for {self.event.name}"