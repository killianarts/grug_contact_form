from django import forms
from django.core.mail import send_mail


def format_message(name, email, message):
    return f"{name}\n{email}\n\n{message}"


def format_subject(name, email):
    return f"[KILLIAN.arts] {name}, {email}"


class ContactForm(forms.Form):
    name = forms.CharField()
    sender_email = forms.EmailField(label='Email')
    message = forms.CharField(widget=forms.Textarea)

    def send(self):
        sender_name = self.cleaned_data['name']
        sender_email = self.cleaned_data['sender_email']
        message = self.cleaned_data['message']
        formatted_subject = format_subject(sender_name, sender_email)
        formatted_message = format_message(sender_name, sender_email, message)
        send_mail(formatted_subject,
                  formatted_message,
                  'noreply@killianarts.online',
                  ['contact@killianarts.online'],
                  )
