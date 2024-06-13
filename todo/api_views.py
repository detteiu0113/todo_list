from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from .models import TodoItem
from .serializers import TodoItemSerializer

class TodoItemViewSet(ModelViewSet):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer

class TodoItemCompleteView(UpdateAPIView):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.completed = True
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)