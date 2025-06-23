
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.arduino_index, name='arduino'),
    path('upload/', views.upload, name='upload'),
    path('api/latest/', views.get_latest_data, name='get_latest_data')
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)