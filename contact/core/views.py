from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .forms import ContactForm
from django.views.decorators.http import require_POST
from django.views.generic import FormView, TemplateView
from django.shortcuts import redirect


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


class ContactPageView(FormView):
    template_name = 'contact_page.html'
    base_template = 'contact_form_partial.html'
    extra_context = {'base_template': base_template}
    form_class = ContactForm
    success_url = '/confirm/'


class ConfirmationView(FormView):
    template_name = 'confirmation_page.html'
    base_template = 'contact_form_partial.html'
    extra_context = {'base_template': base_template}
    form_class = ContactForm
    success_url = '/success/'

    def post(self, request, *args, **kwargs):
        return render(self.request, self.template_name, self.get_context_data())


class SuccessView(FormView):
    template_name = 'success_page.html'
    base_template = 'contact_form_partial.html'
    extra_context = {'base_template': base_template}
    form_class = ContactForm

    def form_valid(self, form):
        form.send()
        return render(self.request, self.template_name, self.get_context_data())
