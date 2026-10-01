from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from django.urls import reverse_lazy
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# Create your views here.
class PostListView(ListView):  # GET Request -> List
    # template_name attribute renders a specific html
    template_name = "postsTemplates/list.html"

    # models attribute let django know from which model (table) we want to retrieve the data
    model = Post

    # context_object_name attribute allows us to change the variable name on how we call it inside of the template
    context_object_name = "posts"

class PostDetailView(LoginRequiredMixin, DetailView):  # GET Request -> Single Object
    template_name = "postsTemplates/detail.html"
    model = Post
    context_object_name = "single_post"

class PostCreateView(LoginRequiredMixin, CreateView):  # GET Request first -> Display Empty form
    # POST Request second -> Create new object
    template_name = "postsTemplates/new.html"
    model = Post
    # fields attribute is a list that allow us to enable/disable the inputs to render in the html
    fields = ["title", "subtitle", "body"]

    def form_valid(self, form):
        # This function help us to run some validations before we create the object
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):  # GET Request first -> Display filled form
    # POST Request second -> Update modified item
    template_name = "postsTemplates/edit.html"
    model = Post
    fields = ["title", "subtitle", "body"]

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "postsTemplates/delete.html"
    model = Post

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


    # success_url attribute allow us to redirect the user to other view if the request was successful
    success_url = reverse_lazy("post_list")