from django.urls import path
from .views import (
    TaskList, TaskDetail, TaskCreate, TaskUpdate, DeleteView,
    CustomLoginView, RegisterPage, TaskReorder, logout_user  # Import the custom logout function
)
#we add urls for each taskviews and each functions in the views.py
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),  # Use the custom logout function
    path('register/', RegisterPage.as_view(), name='register'),

    path('', TaskList.as_view(), name='tasks'),
    #triger the asview method depending on the method type , we need to add it cuz its a class 
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', DeleteView.as_view(), name='task-delete'),
    path('task-reorder/', TaskReorder.as_view(), name='task-reorder'),
]
