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
    time_limit_c = models.IntegerField(default=0)
    time_limit_java = models.IntegerField(default=0)
    memory_limit_c = models.IntegerField(default=0)
    memory_limit_java = models.IntegerField(default=0)
    defunct = models.BooleanField(default=0)
    accepted = models.PositiveIntegerField(default=0)
    submit = models.PositiveIntegerField(default=0)
    solved = models.PositiveIntegerField(default=0)
    type = models.CharField(max_length=20, default="")
    oj = models.CharField(max_length=20)
    judge_type = models.PositiveIntegerField()

    def __unicode__(self):
        return self.title
