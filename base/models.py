from django.db import models
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=1)
    is_active = models.BooleanField(default=False)
    
    # additionally
    image = models.ImageField(upload_to='users/', null=True)
    email = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=50, null=True)
    fullname = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.username


class Book(models.Model):
    title = models.CharField(max_length=70, help_text="The title of the book.")
    image = models.ImageField(upload_to='images/')
    rating = models.IntegerField(help_text="The the reviewer has given.")
    author = models.CharField(max_length=70, help_text="The name of Author")
    price = models.CharField(max_length=10, help_text="Price of book")
    is_published = models.BooleanField(default=False)
    genre = models.CharField(null=True,max_length=70, help_text="The genre of the book.")
    description = models.TextField(help_text="A detailed description of the book.", null=True)
    pages = models.IntegerField(help_text="The number of pages in the book.", null=True)
    publisher = models.CharField(max_length=100, help_text="The publisher of the book.", null=True)
    publish_date = models.DateField(help_text="The publication date of the book.", null=True)
    language = models.CharField(max_length=50, help_text="The language of the book.", null=True)
    book_type = models.CharField(max_length=50, help_text="The type of the book.", null=True)
   
    def __str__(self):
        return self.title

class Blog(models.Model):
    title = models.CharField(max_length=150, help_text="The title of the blog")
    date = models.DateField(auto_now_add=True)
    publisher = models.CharField(max_length=100, help_text="The publisher of the blog", null=True)
    description = models.TextField(help_text="A description of the blog", null=True)
    image = models.ImageField(upload_to='blogs/')
