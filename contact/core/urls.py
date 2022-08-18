from django.urls import path
from .forms import ContactForm
from .views import ContactView, ContactDataPreview, ContactSuccessView

urlpatterns = [
    path('', ContactView.as_view(), name='contact_page'),
    path('confirm/', ContactDataPreview(ContactForm)),
    path('success/', ContactSuccessView.as_view(), name='success_page')
]