from django.urls import path
from . import views

app_name = 'signoff'

urlpatterns = [
    path('', views.signoff_view, name='form'),
    path('thanks/', views.thanks_view, name='thanks'),
]
