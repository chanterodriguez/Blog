from django.views.generic import TemplateView

# Create your views here.
class HomePageView(TemplateView):
    template_name = "pagesTemplates/home.html"
    
class AboutPageView(TemplateView):
    template_name = "pagesTemplates/about.html"

class ContactPageView(TemplateView):
    template_name = "pagesTemplates/contact.html"