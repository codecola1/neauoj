__author__ = 'Code_Cola'

from django import forms
from models import Solve


class SubmitForm(forms.ModelForm):
    error_messages = {
        'code': 'Code is too short',
        'language': "Language can not be empty"
    }

    language_choice = (
        (u'', u'Language'),
        (u'c', u'C'),
        (u'c++', u'C++'),
        (u'java', u'Java'),
    )

    language = forms.ChoiceField(
        error_messages={'required': 'Your language is Required'},
        choices=language_choice,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Solve
        fields = ('problem', 'language', 'code')
        widgets = {
            'problem': forms.TextInput(attrs={'style': 'width: 40%'}),
        }

    def clean_code(self):
        code = self.cleaned_data.get("code")
        if len(code) < 10:
            raise forms.ValidationError(
                self.error_messages['code'],
                code='code_error'
            )
        return code

    def clean_language(self):
        language = self.cleaned_data.get("language")
        if not language or language == 'Language':
            raise forms.ValidationError(
                self.error_messages['language'],
                code='language_error'
            )
        return language