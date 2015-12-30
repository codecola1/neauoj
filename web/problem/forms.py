__author__ = 'Code_Cola'

from django import forms
from problem.models import Problem
import os


class Add_problem_form(forms.ModelForm):
    judge_type_choice = (
        (u'0', u'ACM'),
    )

    judge_type = forms.ChoiceField(
        error_messages={'required': 'Type can not be empty'},
        choices=judge_type_choice,
        widget=forms.Select()
    )

    inputdata = forms.CharField()
    outputdata = forms.CharField()

    class Meta:
        model = Problem
        fields = (
        'title', 'description', 'input', 'output', 'sample_input', 'sample_output', 'hint', 'source', 'memory_limit_c',
        'time_limit_c')

    def save(self, commit=True):
        problem_id = len(Problem.objects.filter(judge_type='0')) + 1000
        title = self.cleaned_data.get("title")
        description = self.cleaned_data.get("description")
        Input = self.cleaned_data.get("input")
        Output = self.cleaned_data.get("output")
        sample_input = self.cleaned_data.get("sample_input")
        sample_output = self.cleaned_data.get("sample_output")
        inputdata = self.cleaned_data.get("inputdata")
        outputdata = self.cleaned_data.get("outputdata")
        hint = self.cleaned_data.get("hint")
        source = self.cleaned_data.get("source")
        type = ''
        oj = 'neau'
        judge_type = self.cleaned_data.get("judge_type")
        memory_limit = self.cleaned_data.get("memory_limit_c")
        time_limit = self.cleaned_data.get("time_limit_c")
        problem = Problem(
            problem_id=problem_id,
            title=title,
            description=description,
            input=Input,
            output=Output,
            sample_input=sample_input,
            sample_output=sample_output,
            hint=hint,
            source=source,
            defunct='0',
            submit='0',
            solved='0',
            type=type,
            oj=oj,
            judge_type=judge_type,
            memory_limit_c=str(int(memory_limit) * 1024),
            memory_limit_java=str(int(memory_limit) * 1024),
            time_limit_c=time_limit,
            time_limit_java=str(int(time_limit) * 2)
        )
        problem.save()
        path = os.getcwd().split('/')[1:-1]
        path = '/' + os.path.join('/'.join(path), 'data', str(problem.id))
        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except:
                return problem
        fp = open(path + '/data.in', 'w')
        fp.write(inputdata)
        fp.close()
        fp = open(path + '/data.out', 'w')
        fp.write(outputdata)
        fp.close()
        return problem