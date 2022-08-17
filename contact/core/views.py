from django.http import HttpResponse
from django.template import loader
from .forms import ContactForm


def contact_page_view(request):
    template = loader.get_template('contact_page.html')
    form = ContactForm()
    context = {
        'form': form
    }
    return HttpResponse(template.render(context, request))