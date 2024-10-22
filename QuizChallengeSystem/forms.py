from django import forms
from .models import Choice


class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions', None)
        super(QuizForm, self).__init__(*args, **kwargs)

        if questions:
            for question in questions:
                choice_list = [(choice.id, f"({chr(65 + index)}) {choice.text}")
                               for index, choice in enumerate(question.choices.all())]

                self.fields[f"question_{question.id}"] = forms.ChoiceField(
                    choices=choice_list,
                    widget=forms.RadioSelect,
                    label=question.text
                )
