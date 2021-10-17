from django.urls import include, path

from z_gram import views

urlpatterns = [
    path('', views.home, name='home'),
]