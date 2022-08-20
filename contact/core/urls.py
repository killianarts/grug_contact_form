from django.urls import path
from .forms import ContactForm
from . import views

urlpatterns = [
    path('', views.contact_page_view, name='contact_page'),
    path('confirm/', views.confirmation_view),
    path('success/', views.send_view)
]