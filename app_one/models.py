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
    posted_by = models.ForeignKey(User, related_name='has_movies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MovieManager()


class CinoRoom(models.Model):
    ROOM_CHOICES = [
        ('A1', 'A1'),
        ('A2', 'A2'),
        ('A3', 'A3'),
        ('B1', 'B1'),
        ('B2', 'B2'),
        ('B3', 'B3'),
        ('C1', 'C1'),
        ('C2', 'C2'),
        ('C3', 'C3'),
        
    ]
    room = models.CharField(max_length=2, choices = ROOM_CHOICES, default='A1')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class MovieShowTime(models.Model):
    date = models.DateField()
    movie = models.ForeignKey(Movie, related_name='movie', on_delete = models.CASCADE)
    room = models.ForeignKey(CinoRoom, related_name='movie_room', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)
           
    
class Booking(models.Model):
    tickets = models.IntegerField()
    price = models.DecimalField(max_digits=4, decimal_places=2)
    booking = models.ForeignKey(MovieShowTime, related_name='showtime', on_delete = models.CASCADE)
    buyer = models.ForeignKey(User, related_name='has_tickets', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  
    
    
class Review(models.Model):
    rating = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    review = models.ForeignKey(Movie, related_name='has_reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
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
    movie = models.ForeignKey(Movie, related_name='has_comments', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()
    
    


    
    
    
    
    