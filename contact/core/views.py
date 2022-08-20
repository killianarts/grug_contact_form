from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .forms import ContactForm
from django_htmx.middleware import HtmxDetails
from django.views.decorators.http import require_POST

class ContactView(TemplateView):
    template_name = 'contact_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm()
        return context


class ContactDataPreview(FormPreview):
    preview_template = 'confirmation_page.html'

    def done(self, request, cleaned_data):
        sender_name = cleaned_data['name']
        sender_email = cleaned_data['sender_email']
        message = cleaned_data['message']
        send_mail(f'{sender_name} - {sender_email}',
                  message,
                  'noreply@killianarts.online',
                  ['contact@killianarts.online'],
                  )
        return HttpResponseRedirect(reverse('success_page'))


class ContactSuccessView(TemplateView):
    template_name = 'success_page.html'
