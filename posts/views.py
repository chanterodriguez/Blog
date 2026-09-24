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


# Create your views here.
class PostListView(ListView):  # GET Request -> List
    # template_name attribute renders a specific html
    template_name = "postsTemplates/list.html"

    # models attribute let django know from which model (table) we want to retrieve the data
    model = Post

    # context_object_name attribute allows us to change the variable name on how we call it inside of the template
    context_object_name = "posts"

class PostDetailView(DetailView):  # GET Request -> Single Object
    template_name = "postsTemplates/detail.html"
    model = Post
    context_object_name = "single_post"

class PostCreateView(CreateView):  # GET Request first -> Display Empty form
                                   # POST Request second -> Create new object
    template_name = "postsTemplates/new.html"
    model = Post
    # fields attribute is a list that allow us to enable/disable the inputs to render in the html
    fields = ["title", "subtitle", "body"]

    def form_valid(self, form):
        # This function help us to run some validations before we create the object
        form.instance.author = User.objects.last()
        return super().form_valid(form)

class PostUpdateView(UpdateView):  # GET Request first -> Display filled form
    # POST Request second -> Update modified item
    template_name = "postsTemplates/edit.html"
    model = Post
    fields = ["title", "subtitle", "body"]


class PostDeleteView(DeleteView):
    template_name = "postsTemplates/delete.html"
    model = Post

    # success_url attribute allow us to redirect the user to other view if the request was successful
    success_url = reverse_lazy("post_list")