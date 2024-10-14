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


ChoiceFormSet = inlineformset_factory(
    Question, Choice,
    fields=('choice_text',),
    extra=5,
    max_num=5,
    can_delete=False,
    widgets={'choice_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le texte du choix'})}
)