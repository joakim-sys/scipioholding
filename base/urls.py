from django.urls import path
from .views import Success, contact


urlpatterns = [
    path('contact/',contact,name='contact'),
    path('success/',Success.as_view(),name='success')
]
