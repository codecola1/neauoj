from django.db import models
from problem.models import Problem
from django.contrib.auth.models import User

# Create your models here.


class In_Problem(models.Model):
    problem = models.ForeignKey(Problem)
    problem_new_id = models.CharField(max_length=20)
    title = models.CharField(max_length=50)

    def __unicode__(self):
        return self.problem_new_id


class Discuss(models.Model):
    problem = models.ForeignKey(In_Problem)
    user = models.ForeignKey(User)
    content = models.TextField(max_length=500)
    time = models.DateTimeField(auto_now_add=True)
    first = models.BooleanField()

    def __unicode__(self):
        return self.content


class Judger(models.Model):
    user = models.ForeignKey(User)


class Contest(models.Model):
    title = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    length = models.TimeField()
    defunct = models.BooleanField(default=False)
    description = models.TextField(max_length=200, blank=True)
    private = models.BooleanField()
    password = models.CharField(max_length=50, blank=True)
    impose = models.BooleanField(default=False)
    type = models.IntegerField()
    creator = models.ForeignKey(User, default=None)
    problem = models.ManyToManyField(In_Problem)
    judger = models.ManyToManyField(Judger)
    discusses = models.ManyToManyField(Discuss)

    def __unicode__(self):
        return self.title