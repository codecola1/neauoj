from django.db import models
from django.contrib.auth.models import User
from status.models import Solve

# Create your models here.

class News(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=500)
    defunct = models.BooleanField(default=False)
    time = models.TimeField()
    def __unicode__(self):
        return self.title

class Judge_account(models.Model):
    oj = models.CharField(max_length=20)
    user_index = models.IntegerField(default=-1)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    defunct = models.BooleanField(default=False)
    def __unicode__(self):
        return self.oj