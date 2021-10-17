from django.urls import include, path

from z_gram import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
