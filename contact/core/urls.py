from django.urls import path
from .forms import ContactForm
from .views import ContactView, ContactDataPreview, ContactSuccessView

urlpatterns = [
    path('', ContactView.as_view(), name='contact_page'),
    path('confirm/', ContactDataPreview(ContactForm)),
    # path('confirm', views.confirmation_page_view, name='confirmation_page'),
    path('submit/', ContactSuccessView.as_view(), name='success_page')
]