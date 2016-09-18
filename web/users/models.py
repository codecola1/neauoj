from django.db import models
from django.contrib.auth.models import User
from problem.models import Problem

# Create your models here.


class submit_problem(models.Model):
    user = models.ForeignKey(User)
    ac = models.BooleanField(default=False)
    problem = models.ForeignKey(Problem)

    def __unicode__(self):
        return self.user.username


class OJ_account(models.Model):
    oj = models.CharField(max_length=20)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    last_rid = models.CharField(max_length=15, default=0)
    is_using = models.BooleanField(default=False)
    updating = models.IntegerField(default=0)
    defunct = models.BooleanField(default=False)

    def __unicode__(self):
        return self.username


class Info(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=50)
    school = models.CharField(max_length=20, default="None")
    grade = models.PositiveIntegerField()
    team = models.BooleanField(default=False)
    classes = models.CharField(max_length=20, default="None")
    real_name = models.CharField(max_length=20, default="None")
    qq = models.CharField(max_length=15, default="None")
    status = models.IntegerField(default=0)
    oj_account = models.ManyToManyField(OJ_account)
    telephone = models.CharField(max_length=20, default="None")
    student_id = models.CharField(max_length=20, default="None")

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
