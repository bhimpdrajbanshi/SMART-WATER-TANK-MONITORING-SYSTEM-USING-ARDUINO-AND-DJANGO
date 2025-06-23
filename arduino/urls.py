
from django.urls import path
from . import views

urlpatterns = [
    path('', views.arduino_index, name='arduino'),
    path('upload/', views.upload, name='upload'),
    path('api/latest/', views.get_latest_data, name='get_latest_data')
]
