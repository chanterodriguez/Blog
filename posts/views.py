from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
    View
    )
from .forms import CommentForm
from django.urls import reverse_lazy, reverse
from .models import Post, Status
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.detail import SingleObjectMixin


# Create your views here.
class PostListView(ListView):  # GET Request -> List
    # template_name attribute renders a specific html
    template_name = "postsTemplates/list.html"

    # models attribute let django know from which model (table) we want to retrieve the data
    model = Post

    # context_object_name attribute allows us to change the variable name on how we call it inside of the template
    context_object_name = "posts"

    def get_queryset(self):
        status = Status.objects.get(name="Published")
        return Post.objects.filter(status=status).order_by("created_on")

class PostArchivedListView(LoginRequiredMixin, ListView):  # GET Request -> List of archived posts
    template_name = "postsTemplates/list.html"
    model = Post
    context_object_name = "posts"

    def get_queryset(self):
        # Only archived posts that belong to the logged in user
        status = Status.objects.get(name="Archive")
        return Post.objects.filter(status=status, author=self.request.user).order_by("created_on")

class PostDraftListView(LoginRequiredMixin, ListView):  # GET Request -> List of draft posts
    template_name = "postsTemplates/list.html"
    model = Post
    context_object_name = "posts"

    def get_queryset(self):
        # Only draft posts that belong to the logged in user
        status = Status.objects.get(name="Draft")
        return Post.objects.filter(status=status, author=self.request.user).order_by("created_on")


# --------Comment Section ---------
class PostView(View):
    def get(self, request, *args, **kwargs):
        view = PostDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostCommentFormView.as_view()
        return view(request, *args, **kwargs)


class PostDetailView(LoginRequiredMixin, DetailView):  # GET Request -> Single Object
    template_name = "postsTemplates/detail.html"
    model = Post
    context_object_name = "single_post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        return context


class PostCommentFormView(SingleObjectMixin, FormView):
    template_name = "postsTemplates/detail.html"
    form_class = CommentForm
    model = Post

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.save()  # needs a PK before the many-to-many .add() below works
        comment.posts.add(self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})


# --------Emd Comment Section --------


class PostCreateView(LoginRequiredMixin, CreateView):  # GET Request first -> Display Empty form
    # POST Request second -> Create new object
    template_name = "postsTemplates/new.html"
    model = Post
    # fields attribute is a list that allow us to enable/disable the inputs to render in the html
    fields = ["title", "subtitle", "body", "status", ]

    def form_valid(self, form):
        # This function help us to run some validations before we create the object
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):  # GET Request first -> Display filled form
    # POST Request second -> Update modified item
    template_name = "postsTemplates/edit.html"
    model = Post
    fields = ["title", "subtitle", "body","status"]

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