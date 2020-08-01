from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime, date
from django.db import models
import bcrypt
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):                
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors['password'] ='Password should be at least 8 characters'
        if postData['password'] != postData['conf_password']:
            errors['conf_password'] = 'Passwords should match'         
        result = User.objects.filter(email=postData['email'])
        if len(result) > 0:
            errors['email'] = 'Email has already been registered!'
            
        return errors
    

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10, default='0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
    
class MovieManager(models.Manager):
    def movie_validator(self, postData):
        errors = {}     
        if len(postData['title']) < 2:
            errors["title"] = "Title should be at least 2 characters"
        if len(postData['desc']) < 10:
            errors["desc"] = "Description should be at least 10 characters"            
        return errors

class Movie(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    likes = models.ManyToManyField(User, related_name='has_likes')
    cover_image = models.ImageField(upload_to="images", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video_url = models.TextField()
    objects = MovieManager()

class CinoRoom(models.Model):
    room = models.CharField(max_length=2, default='A1')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class ShowTime(models.Model):
    date = models.DateField()
    tickets = models.IntegerField()
    price = models.DecimalField(max_digits=4, decimal_places=2)   
    time = models.TimeField(auto_now=True)
    movie = models.ForeignKey(Movie, related_name='has_show_times', on_delete = models.CASCADE)
    room = models.ForeignKey(CinoRoom, related_name='has_show_times', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)
           
    
class Booking(models.Model):
    tickets = models.IntegerField()
    price = models.DecimalField(max_digits=4, decimal_places=2)   
    buyer = models.ForeignKey(User, related_name='has_bookings', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

class Seat(models.Model):
    row = models.CharField(max_length=2)
    number = models.IntegerField()
    room = models.ForeignKey(CinoRoom, related_name="has_seats", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

class Seat_booked(models.Model):
    seat = models.ForeignKey(Seat, related_name="has_seats_booked", on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, related_name="has_seats_booked", on_delete=models.CASCADE)
    show_time = models.ForeignKey(ShowTime, related_name="has_seats_booked", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  
    

# Movie related 
class Review(models.Model):
    rating = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    for_movie = models.ForeignKey(Movie, related_name='has_reviews', on_delete=models.CASCADE)
    posted_by = models.ForeignKey(User, related_name='has_reviews', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class CommentManager(models.Manager):
    def comm_validator(self, postData):
        errors = {}     
        if len(postData['content']) < 5:
            errors["content"] = "Content should be at least 5 characters"          
        return errors
       
class Comments(models.Model):
    content = models.TextField()
    posted_by = models.ForeignKey(User, related_name='has_comments', on_delete=models.CASCADE)
    for_movie = models.ForeignKey(Movie, related_name='has_comments', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()
    
    
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
    likes = models.ManyToManyField(User, related_name='likes_events')
    cover_image = models.ImageField(upload_to="images", blank=True)   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
