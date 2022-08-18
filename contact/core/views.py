from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from .forms import ContactForm
from django.views.generic import TemplateView
from formtools.preview import FormPreview


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
