from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from .models import TodoItem
from accounts.models import CustomUser

class TodoListView(LoginRequiredMixin, ListView):
    model = TodoItem
    context_object_name = 'todos'
    template_name = 'todo/todo_list.html'

    def get_queryset(self):
        # モデルオブジェクトのクエリセットを取得し、指定された順序で並べ替える
        return super().get_queryset().order_by('user_id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 0は未分類用
        context['user_list'] = [0] + list(CustomUser.objects.all())
        context['todo_list'] = TodoItem.objects.all()

        # 現在のToDoアイテムの一番大きいIDを取得して、次のIDを計算する
        max_id = TodoItem.objects.aggregate(max_id=models.Max('id'))['max_id']
        max_todo_id =  max_id if max_id else 0
        next_todo_id = max_todo_id + 1
        context['next_todo_id'] = next_todo_id
        return context