from django.db import models
from django.contrib.auth.models import User,AbstractUser

# Create your models here.

class Account(models.Model):
    user = models.ForeignKey(User)
    oj = models.CharField(max_length=20)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    last = models.PositiveIntegerField()
    submit = models.PositiveIntegerField(default=0)
    solved = models.PositiveIntegerField(default=0)
    defunct = models.BooleanField(default=False)
    def __unicode__(self):
        return self.username

class Info(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=50)
    submit = models.PositiveIntegerField(default=0)
    solve = models.PositiveIntegerField(default=0)
    submit_in = models.PositiveIntegerField(default=0)
    solve_in = models.PositiveIntegerField(default=0)
    submit_out = models.PositiveIntegerField(default=0)
    solve_out = models.PositiveIntegerField(default=0)
    school = models.CharField(max_length=20)
    grade = models.PositiveIntegerField()
    team = models.BooleanField(default=False)
    account = models.ManyToManyField(Account)
    def __unicode__(self):
        return self.user.username

class Message(models.Model):
    user = models.ForeignKey(User)
    from_user = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=500)
    is_new = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.title