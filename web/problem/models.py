from django.db import models

# Create your models here.

class Problem(models.Model):
    problem_id = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=2000)
    input = models.TextField(max_length=2000)
    output = models.TextField(max_length=2000)
    sample_input = models.TextField(max_length=500)
    sample_output = models.TextField(max_length=500)
    hint = models.TextField(max_length=500)
    source = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    time_limit = models.IntegerField()
    memory_limit = models.IntegerField()
    defunct = models.BooleanField()
    accepted = models.PositiveIntegerField()
    submit = models.PositiveIntegerField()
    solved = models.PositiveIntegerField()
    type = models.CharField(max_length=20)
    oj = models.CharField(max_length=20)
    judge_type = models.PositiveIntegerField()
    def __unicode__(self):
        return self.title
