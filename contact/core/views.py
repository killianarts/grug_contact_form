from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .forms import ContactForm
from django.views.decorators.http import require_POST
from django.views.generic import FormView


def contact_page_view(request: HttpRequest) -> HttpResponse:
    template = 'contact_page.html'
    base_template = 'contact_form_partial.html'
    form = ContactForm()
    context = {
        'form': form,
        'base_template': base_template,
    }
    return render(request, template, context)


@require_POST
def confirmation_view(request: HttpRequest) -> HttpResponse:
    template = 'confirmation_page.html'
    base_template = 'contact_form_partial.html'
    form = ContactForm(request.POST)
    context = {
        'form': form,
        'base_template': base_template,
    }
    if form.is_valid():
        return render(request, template, context)


@require_POST
def send_view(request: HttpRequest) -> HttpResponse:
    template = 'success_page.html'
    base_template = 'contact_form_partial.html'
    form = ContactForm(request.POST)
    context = {
        'form': form,
        'base_template': base_template,
    }
    if form.is_valid():
        form.send()
    return render(request, template, context)