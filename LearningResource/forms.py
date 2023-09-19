from django import forms

from .models import SubModule, LearningModule


class SubModuleForm(forms.ModelForm):
    class Meta:
        model = SubModule
        fields = [
            'name',
            'difficulty_level',
            'description',
            'parent_module'
        ]


class LearningModuleForm(forms.ModelForm):
    class Meta:
        model = LearningModule
        fields = [
            'name',
            'description'
        ]
