from django import forms

from .models import essay, essay_type


# 类型添加
class addTypeForm(forms.Form):
    class Meta:
        model = essay_type
        fields = ['type']
