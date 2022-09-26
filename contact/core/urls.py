from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path('', views.contact_page, name='contact_page'),
    path('confirm/', views.validate_then_confirm),
    path('send/', views.send_form)
]
