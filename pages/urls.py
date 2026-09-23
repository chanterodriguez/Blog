from django.urls import path
from .views import HomePageView, AboutPageView, contact_page

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("contact/", contact_page, name="contact"),
]