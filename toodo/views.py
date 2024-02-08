from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PrivateTodo, PublicTodo, Upvote, Notification
from .forms import PrivateTodoForm, PrivateTodoCompletedForm, PublicTodoUpvotesForm
from django.utils import timezone
from django.http import QueryDict, JsonResponse, HttpResponseBadRequest
from django.core.exceptions import ValidationError

@login_required
def index(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.method == 'POST' and request.POST.__contains__('todo_text'):
            form = PrivateTodoForm(request.POST)
            try:
                if form.is_valid():
                    PublicTodo.objects.create(user=request.user,
                                todo_text=form.cleaned_data['todo_text'],
                                pub_date=timezone.now())
                    return JsonResponse({'status': 'Shared!'})
            except ValidationError:
                return JsonResponse({'status': 'Invalid request'}, status=400)
        return JsonResponse({'status': 'Invalid request'}, status=400)
    elif request.method == 'GET':
        public_todos = PublicTodo.objects.all()
        return render(request, 'toodo/public.html', {'public_todos': public_todos})
    return HttpResponseBadRequest('Invalid request')

@login_required
def public_update(request, todo_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        todo_update = get_object_or_404(PublicTodo, pk=todo_id)
        if request.method == 'PUT':
            put = QueryDict(request.body)
            if put.__contains__('upvotes'):
                form = PublicTodoUpvotesForm(put)
                try:
                    if form.is_valid():
                        todo_update.upvotes = form.cleaned_data['upvotes']
                        todo_update.save()
                        u = Upvote(public_todo=todo_update, user=request.user)
                        u.save()
                        n = Notification(action=1, sender=request.user, receiver=todo_update.user, timestamp=timezone.now())
                        n.save()
                    return JsonResponse({'updated': todo_id})
                except ValidationError:
                    return JsonResponse({'status': 'Invalid request'}, status=400)
            return JsonResponse({'status': 'Invalid request'}, status=400)
        return JsonResponse({'status': 'Invalid request'}, status=400)
    return HttpResponseBadRequest('Invalid request')
    
@login_required
def private(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST' and (request.POST.__contains__('todo_text[]') or request.POST.__contains__('todo_text')): 
        if request.POST.__contains__('todo_text[]'):
            todos = request.POST.getlist('todo_text[]') 
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
        else:
            form = PrivateTodoForm(request.POST)
            try:
                if form.is_valid():
                    t = PrivateTodo(user=request.user, todo_text=form.cleaned_data['todo_text'], pub_date=timezone.now()) 
                    t.save()
                return JsonResponse({'status': 'Added!'})
            except ValidationError:
                return JsonResponse({'status': 'Invalid request'}, status=400)
    elif request.method == 'GET':
        private_todos = PrivateTodo.objects.filter(user=request.user)
        return render(request, 'toodo/private.html', {'private_todos': private_todos})
    return HttpResponseBadRequest('Invalid request')

@login_required
def private_update(request, todo_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        todo_update = get_object_or_404(PrivateTodo, pk=todo_id)
        if request.method == 'DELETE':
            todo_update.delete()
            return JsonResponse({'deleted': todo_id})
        elif request.method == 'PUT':
            put = QueryDict(request.body)
            if put.__contains__('todo_text'):
                form = PrivateTodoForm(put)
                try:
                    if form.is_valid():
                        todo_update.todo_text = form.cleaned_data['todo_text']
                        todo_update.pub_date = timezone.now()
                        todo_update.save()
                    return JsonResponse({'updated': todo_id})
                except ValidationError:
                    return JsonResponse({'status': 'Invalid request'}, status=400)
            elif put.__contains__('completed'):
                form = PrivateTodoCompletedForm(put)
                try:
                    if form.is_valid():
                        todo_update.completed = form.cleaned_data['completed']
                        todo_update.save()
                    return JsonResponse({'updated': todo_id})
                except ValidationError:
                    return JsonResponse({'status': 'Invalid request'}, status=400)
            return JsonResponse({'status': 'Invalid request'}, status=400)
        return JsonResponse({'status': 'Invalid request'}, status=400)
    return HttpResponseBadRequest('Invalid request')



            