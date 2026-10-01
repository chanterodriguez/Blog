from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import SignUpForm


# Create your views here.
class SignUpView(CreateView):
    template_name = "registration/signup.html"

    # form_class attribute allow us to create objects from a form file
    # we use this one when we want to have a custom form
    form_class = SignUpForm
    success_url = reverse_lazy("login")