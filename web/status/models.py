from django.db import models
from django.contrib.auth.models import User
from problem.models import Problem

# Create your models here.

class Solve(models.Model):
    user = models.ForeignKey(User)
    problem = models.ForeignKey(Problem)
    run_id = models.PositiveIntegerField()
    submit_time = models.DateTimeField()
    status = models.CharField(max_length=20)
    use_time = models.IntegerField()
    use_memory = models.IntegerField()
    language = models.CharField(max_length=20)
    length = models.IntegerField()
    wait_show = models.BooleanField(default=True)
    is_site = models.BooleanField(default=True)
    code = models.TextField(max_length=5000, default="")
    def __unicode__(self):
        return self.problem.title

class ce_info(models.Model):
    solve = models.ForeignKey(Solve)
    info = models.TextField(max_length=500)
    def __unicode__(self):
        return self.solve.problem.title

class Solve_first(models.Model):
    user = models.ForeignKey(User)
    problem = models.ForeignKey(Problem)
    solve = models.ForeignKey(Solve)
    def __unicode__(self):
        return self.problem.title