from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Post(models.Model):
    author = models.ForeignKey(User, verbose_name=("author"), on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()
    image = models.ImageField()
    date = models.DateTimeField()
    likes = models.IntegerField()

    def __str__(self):
        return self.title
    
class News(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return self.title

class NH(models.Model):
    image = models.ImageField()
    