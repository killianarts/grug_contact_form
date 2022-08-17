from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.template import loader
from .forms import ContactForm


def contact_page_view(request):
    template = loader.get_template('contact_page.html')
    form = ContactForm()
    context = {
        'form': form
    }
    return HttpResponse(template.render(context, request))


@require_POST
def confirmation_view(request):
    template = loader.get_template('confirmation_page.html')
    form = ContactForm(request.POST)
    context = {
        'form': form
    }
    return HttpResponse(template.render(context, request))