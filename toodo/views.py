import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PrivateTodo, PublicTodo
from .forms import PrivateTodoForm
from django.utils import timezone
from django.http import HttpResponseRedirect, QueryDict, JsonResponse, HttpResponseBadRequest
from django.urls import reverse
from django.core.exceptions import ValidationError

@login_required
def index(request):
    public_todos = PublicTodo.objects.all()
    return render(request, 'toodo/public.html', {'public_todos': public_todos})

def private(request):
    # private_todos = PrivateTodo.objects.filter(user=request.user)
    # return render(request, 'toodo/private.html', {'private_todos': private_todos})
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST' and request.POST.__contains__('todo_text'): 
        todos = request.POST.getlist('todo_text') 
        print(todos)
        forms = []
        for todo in todos:
            form = PrivateTodoForm(QueryDict("todo_text=" + todo))
            try:
                if form.is_valid():
                    forms.append(form)
            except ValidationError:
                return HttpResponseBadRequest('Invalid request')
        new_todos = []
        for form in forms:
            todo_text = form.cleaned_data['todo_text']
            t = PrivateTodo(user=request.user, todo_text=todo_text, pub_date=timezone.now()) 
            t.save()
            new_todos.append(t) 
        print(str(len(new_todos)) + ' todo(s) added!')
        return render(request, 'toodo/todo_items.html', {'todos': new_todos})
    elif request.method == 'GET':
        private_todos = PrivateTodo.objects.filter(user=request.user)
        return render(request, 'toodo/private.html', {'private_todos': private_todos})
    else:
        return HttpResponseBadRequest('Invalid request')

@login_required
def private_create(request):
    if request.method == 'POST' and request.POST.__contains__('todo_text'):
        print(request.POST)
        for todo in request.POST.getlist('todo_text'):
            form = PrivateTodoForm(QueryDict("todo_text=" + todo))
            if form.is_valid():
                todo_text = form.cleaned_data['todo_text']
                PrivateTodo.objects.create(user=request.user,
                                            todo_text=todo_text,
                                            pub_date=timezone.now()) 
    return HttpResponseRedirect(reverse('toodo:private'))

@login_required
def private_update(request, todo_id):
    if request.method == 'POST':
        form = PrivateTodoForm(request.POST)
        if form.is_valid():
            todo_edit = get_object_or_404(PrivateTodo, pk=todo_id)
            todo_edit.todo_text = form.cleaned_data['todo_text']
            todo_edit.pub_date = timezone.now()
            todo_edit.save()
    return HttpResponseRedirect(reverse('toodo:private'))

@login_required
def private_delete(request, todo_id):
    if request.method == 'POST':
        todo_delete = get_object_or_404(PrivateTodo, pk=todo_id)
        todo_delete.delete()
    return HttpResponseRedirect(reverse('toodo:private'))

@login_required
def private_completed(request, todo_id):
    if request.method == 'POST':
        todo_completed = get_object_or_404(PrivateTodo, pk=todo_id)
        if todo_completed.completed:
            todo_completed.completed = False
        else:
            todo_completed.completed = True
        todo_completed.save()
    return HttpResponseRedirect(reverse('toodo:private'))

@login_required
def private_share(request, todo_id):
    if request.method == 'POST':
        todo_share = get_object_or_404(PrivateTodo, pk=todo_id)
        PublicTodo.objects.create(user=request.user,
                                        todo_text=todo_share.todo_text,
                                        pub_date=timezone.now())
    return HttpResponseRedirect(reverse('toodo:private'))
            