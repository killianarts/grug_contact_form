from django import forms


class ContactForm(forms.Form):
    name = forms.CharField()
    sender_email = forms.EmailField(label='Email')
    message = forms.CharField(widget=forms.Textarea)
