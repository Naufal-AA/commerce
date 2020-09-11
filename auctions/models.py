from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    gender = models.CharField(max_length=10, default='')
    address = models.CharField(max_length=100, default='')
    phone = models.IntegerField(default=0)
    image = models.ImageField(upload_to='Profile/', blank=True)

    def __str__(self):
        return f"{self.username}"


class Category(models.Model):
    category = models.CharField(max_length=100,unique=True)
    timestamp = models.DateTimeField(auto_now = False, auto_now_add = True)

    def __str__(self):
        return f"{self.category}"


class List(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Listuser")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listcategory")
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(default='', unique=True)
    timestamp = models.DateTimeField(auto_now = False, auto_now_add = True)
    update = models.DateTimeField(auto_now = True, auto_now_add = False)
    startbid = models.DecimalField(max_digits=10, decimal_places=2)
    
    currentbid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    finalbid = models.DecimalField(max_digits=10, decimal_places=2)
    winner = models.TextField(max_length=255, default='',blank=True)
    image = models.ImageField(upload_to='List/', blank=True)
    url = models.TextField(blank=True)
    active = models.BooleanField(default='False')
    close = models.BooleanField(default='False')

    def __str__(self):
        return f"{self.title} start-price: {self.startbid}"

class Bid(models.Model):
    lists = models.ForeignKey(List, on_delete=models.CASCADE, related_name="list")
    participant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="participant")
    bid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    selected = models.BooleanField(default="False")
    timestamp = models.DateTimeField(auto_now = False, auto_now_add = True)
    
    def __str__(self):
        return f"{self.participant} placed ({self.bid}) in {self.lists}"

class Comment(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentname")
    comments = models.ForeignKey(List, on_delete=models.CASCADE, related_name="comment")
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now = False, auto_now_add = True)
    
    def __str__(self):
        return f"{self.name} commented ({self.comment}) in {self.comments}"

class Watchlist(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlistname")
    watchlist = models.ForeignKey(List, on_delete=models.CASCADE, related_name="watchlist")
    watched = models.BooleanField(default="False")
    timestamp = models.DateTimeField(auto_now = False, auto_now_add = True)
    
    def __str__(self):
        return f"{self.name} listed as watchlist:  ({self.watchlist})"

