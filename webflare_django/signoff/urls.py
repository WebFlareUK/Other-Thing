from django.urls import path
from . import views

app_name = 'signoff'

urlpatterns = [
    path('', views.signoff_view, name='form'),
    path('thanks/', views.thanks_view, name='thanks'),
    path('delete/<int:signoff_id>/', views.delete_signoff_view, name='delete'),
    path('delete/confirmation/', views.delete_confirmation_view, name='delete_confirmation'),
]
