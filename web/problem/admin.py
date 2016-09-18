from django.contrib import admin

# Register your models here.

from problem.models import Problem

class ProblemAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'input', 'output', 'sample_input', 'sample_output', 'hint', 'source', 'time_limit', 'memory_limit', 'defunct', 'judge_type')

admin.site.register(Problem)