from django.urls import path
from . import views

# urlpatterns = [
#     path('', views.contact_page_view, name='contact_page'),
#     path('confirm/', views.confirmation_view),
#     path('success/', views.send_view)
# ]

urlpatterns = [
    path('', views.ContactPageView.as_view(), name='contact_page'),
    path('confirm/', views.ConfirmationView.as_view()),
    path('success/', views.SuccessView.as_view())
]