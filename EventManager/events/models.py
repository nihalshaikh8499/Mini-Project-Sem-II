from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils import timezone 

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
    rule_book = models.FileField(upload_to='rule_books/', blank=True, null=True)
    volunteer_requirement = models.PositiveIntegerField(default=0)
    registration_deadline = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.registration_deadline:
            self.registration_deadline = timezone.datetime.combine(self.date, timezone.datetime.min.time()) - timezone.timedelta(days=1)
        super().save(*args, **kwargs)

    def is_registration_expired(self):
        return self.registration_deadline and self.registration_deadline < now()

    def __str__(self):
        return self.name
    
class VolunteerRegistration(models.Model):
    DEPARTMENT_CHOICES = [
        ('FY MCA', 'First Year MCA'),
        ('SY MCA', 'Second Year MCA'),
        ('FY MBA', 'First Year MBA'),
        ('SY MBA', 'Second Year MBA'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)
    department = models.CharField(max_length=10, choices=DEPARTMENT_CHOICES)
    name =  models.CharField(max_length=50)
    rollnumber = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')  

    def __str__(self):
        return f"{self.user.username} volunteering for {self.event.name}"
    
class EventRegistration(models.Model):
    DEPARTMENT_CHOICES = [
        ('FY MCA', 'First Year MCA'),
        ('SY MCA', 'Second Year MCA'),
        ('FY MBA', 'First Year MBA'),
        ('SY MBA', 'Second Year MBA'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)
    department = models.CharField(max_length=10, choices=DEPARTMENT_CHOICES)
    players = models.JSONField()

    class Meta:
        unique_together = ('user', 'event')  

    def __str__(self):
        return f"Registration for {self.event.name} by {self.user.username}"
    
class AllowedEmail(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)

class ContactFormModel(models.Model):
    FORM_CATEGORIES = [
                ('General inquiry','General inquiry'),
                ('Technical support','Technical support'),
                ('Feedback & Suggestion','Feedback & Suggestion'),
                ('Lost & found','Lost & found')
               ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, choices=FORM_CATEGORIES)
    message = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Contact request for {self.subject} from {self.user}"
    
class EventHighlight(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def first_image(self):
        return self.images.first()  

    def __str__(self):
        return self.title


class EventImage(models.Model):
    event = models.ForeignKey(EventHighlight, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_highlights/')

    def __str__(self):
        return f"Image for {self.event.title}"

