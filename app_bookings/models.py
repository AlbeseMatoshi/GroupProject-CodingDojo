from django.db import models
from app_one.models import User

# Events
class EventManager(models.Manager):
      def event_validator(self, postData):
            errors = {}     
            if len(postData['title']) < 2:
                  errors["title"] = "Title should be at least 2 characters"
            if len(postData['desc']) < 5:
                  errors["desc"] = "Description should be at least 5 characters" 
            return errors
    
    
class Event(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    likes = models.ManyToManyField(User, related_name='events_liked')
    cover_image = models.ImageField(upload_to="images", blank=True)   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = EventManager()
    
    
    
