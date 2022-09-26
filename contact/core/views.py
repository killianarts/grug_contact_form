from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .forms import ContactForm
from django.views.decorators.http import require_POST
from render_block import render_block_to_string
from smtplib import SMTPException


def contact_page(request: HttpRequest) -> HttpResponse:
    if request.POST:
        form = ContactForm(request.POST)
        context = {'form': form}
        block = 'contact_form'
        html = render_block_to_string("core/contact_page.html", block, context)
        return HttpResponse(html)
    form = ContactForm()
    context = {'form': form}
    return render(request, 'core/contact_page.html', context)


@require_POST
def validate_then_confirm(request: HttpRequest) -> HttpResponse:
    block = 'contact_form'
    form = ContactForm(request.POST)
    context = {'form': form}
    if form.is_valid():
        html = render_block_to_string('core/form/_confirmation.html', block, context)
        return HttpResponse(html)
    return contact_page(request)


@require_POST
def send_form(request: HttpRequest) -> HttpResponse:
    block = 'contact_form'
    form = ContactForm(request.POST)
    context = {'form': form}
    html = render_block_to_string('core/form/_send.html', block, context)
    if form.is_valid():
        try:
            form.send()
        except SMTPException as error:
            context += {
                'error': error
            }
    return HttpResponse(html)
