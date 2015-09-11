from django.db import models
from django.contrib.auth.models import User
from problem.models import Problem

# Create your models here.

class Solve(models.Model):
    user = models.ForeignKey(User)
    problem = models.ForeignKey(Problem)
    submit_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    use_time = models.IntegerField(default=0)
    use_memory = models.IntegerField(default=0)
    language = models.CharField(max_length=20)
    length = models.IntegerField()
    wait_show = models.BooleanField(default=True)
    code = models.TextField(max_length=5000, default="")

    def __unicode__(self):
        return self.problem.title


class ce_info(models.Model):
    solve = models.ForeignKey(Solve)
    info = models.TextField(max_length=500)

    def __unicode__(self):
        return self.solve.problem.title
