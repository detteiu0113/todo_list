from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import TodoItemViewSet, TodoItemCompleteView

router = DefaultRouter()
router.register(r'', TodoItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/complete/', TodoItemCompleteView.as_view(), name='todo-complete'),
]