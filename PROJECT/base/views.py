from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView #importing all the class based veiws 
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy  #it redirects user to a certain part  of app

from django.contrib.auth.views import LoginView #for the login view 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm #makes sure registerd user no need to login again
from django.contrib.auth import login, logout  # Import login/logout function

# Imports for Reordering Feature
from django.views import View
from django.db import transaction

from .models import Task
from .forms import PositionForm


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)

#add the mixin to not allow them without login 
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
# This part is making sure user only gets thier data and thier tasks
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user) #only values of the user , not others 
        context['count'] = context['tasks'].filter(complete=False).count() 

        search_input = self.request.GET.get('search-area') or ''
       #searching the tasks based on title 
        if search_input:
            context['tasks'] = context['tasks'].filter(title__contains=search_input)

        context['search_input'] = search_input

        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task' 
    template_name = 'base/task.html' #point to app name


class TaskCreate(LoginRequiredMixin, CreateView):
    #attributes of the create
    model = Task
    fields = ['title', 'description', 'complete'] #list down all the fields
    success_url = reverse_lazy('tasks')#redirect user to tasks 

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

#update view 
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks') #redirecting user back 

#renders out a confirmation page and on request it deletes
class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)


class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))


# Function-based logout view
def logout_user(request):
    logout(request)
    return redirect('login')
