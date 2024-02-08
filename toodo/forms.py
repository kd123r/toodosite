from django import forms

class PrivateTodoForm(forms.Form):
    todo_text = forms.CharField(label='Todo', max_length=200)

class PrivateTodoCompletedForm(forms.Form):
    completed = forms.BooleanField(required=False)

class PublicTodoUpvotesForm(forms.Form):
    upvotes = forms.IntegerField()


