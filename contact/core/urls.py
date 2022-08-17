from django.urls import path

from . import views

urlpatterns = [
    path('', views.contact_page_view, name='contact_page'),
]