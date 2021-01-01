from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class SearchHistory(models.Model):
    id = models.AutoField(primary_key=True)
    subreddit = models.CharField(max_length=200)
    keyword = models.CharField(max_length=200)
    timestamp = models.DateTimeField(default=timezone.now)
    subscribed = models.BooleanField(default=False)
    subscribed_frequency = models.IntegerField(default=0)
    latest_search = models.DateTimeField(null=True)
    email = models.CharField(max_length=200, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class AdvancedSearchHistory(models.Model):
    id = models.AutoField(primary_key=True)
    subreddit = models.CharField(max_length=200)
    word_in_title = models.CharField(max_length=200)
    word_not_in_title = models.CharField(max_length=200)
    word_in_comment = models.CharField(max_length=200)
    word_not_in_comment = models.CharField(max_length=200)
    search_within = models.CharField(max_length=200)
    search_limit = models.CharField(max_length=200)
    timestamp = models.DateTimeField(default=timezone.now)
    subscribed = models.BooleanField(default=False)
    subscribed_frequency = models.IntegerField(default=0)
    latest_search = models.DateTimeField(null=True)
    email = models.CharField(max_length=200, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class ShowUsers(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    joined = models.DateTimeField(auto_now=True)
    superuser = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
    
    class Users:
       db_table = "auth_user" 

#class AuthUser(models.Model):
    #id = models.AutoField(primary_key=True)
    #username = models.CharField(max_length=50)
    #email = models.CharField(max_length=50)
    #joined = models.DateTimeField(auto_now=True)
    #superuser = models.CharField(max_length=50)
    #subcribed = models.BooleanField(default=False)
    #subcribed_frequency = models.IntegerField(default=0)
    #user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    #def __str__(self):
        #return self.name
    
    #class Users:
       #db_table = "auth_user" 
    
    