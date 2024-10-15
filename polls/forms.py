from django.forms import inlineformset_factory
from .models import Question, Choice
from django import forms


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']
        labels = {
            'choice_text': 'Entrez les réponses',
        }
        widgets = {
            'choice_text': forms.TextInput()
        }


ChoiceFormSet = inlineformset_factory(
    Question, Choice,
    form=ChoiceForm,
    extra=5,
    max_num=5,
    can_delete=False,
)