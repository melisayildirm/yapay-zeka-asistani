# analiz_uygulamasi/urls.py

from django.urls import path
from . import views # views.py dosyamızı import ediyoruz

app_name = 'analiz_uygulamasi' # Bu uygulamanın URL'leri için benzersiz isim alanı

urlpatterns = [
    path('analiz/', views.analiz_senaryo, name='analiz_senaryo'),
   ]