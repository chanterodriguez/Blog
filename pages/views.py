from django.views.generic import TemplateView
from django.shortcuts import HttpResponse, render

# Create your views here.
class HomePageView(TemplateView):
    template_name = "pagesTemplates/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "Chante'"
        print(context)
        return context

class AboutPageView(TemplateView):
    template_name = "pagesTemplates/about.html"


#Function Based Views
def contact_page(request):
    #print(request.__dict__)
    #return HttpResponse("Hello world from a FBV")

    contact_info = {
        "name": "Chante'",
        "address": "Somewhere else",
        "email": "chante.rodriguez@gmail.com"
    }
    return render(request, "pagesTemplates/contact.html", contact_info)