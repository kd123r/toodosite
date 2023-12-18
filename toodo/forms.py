from django import forms

class PrivateTodoForm(forms.Form):
    todo_text = forms.CharField(label='Todo', max_length=200)

