from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .forms import ContactForm
from django_htmx.middleware import HtmxDetails
from django.views.decorators.http import require_POST

class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails

def contact_page_view(request: HtmxHttpRequest) -> HttpResponse:
    template = 'contact_page.html'
    base_template = 'contact_form_partial.html'
    form = ContactForm()
    context = {
        'form': form,
        'base_template': base_template,
    }
    return render(request, template, context)

@require_POST
def confirmation_view(request: HtmxHttpRequest) -> HttpResponse:
    template = 'confirmation_page.html'
    base_template = 'contact_form_partial.html'
    form = ContactForm(request.POST)
    if form.is_valid():
        context = {
            'form': form,
            'base_template': base_template,
        }
        return render(request, template, context)

@require_POST
def send_view(request: HtmxHttpRequest) -> HttpResponse:
    template = 'success_page.html'
    base_template = 'contact_form_partial.html'
    form = ContactForm(request.POST)
    if form.is_valid():
        form.send()
    else:
        return HttpResponse("Whoops")
    context = {
        'form': form,
        'base_template': base_template,
    }
    return render(request, template, context)