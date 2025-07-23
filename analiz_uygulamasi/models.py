from django.db import models
# analiz_uygulamasi/models.py

from django.db import models
# analiz_uygulamasi/models.py

from django.db import models
from django.contrib.auth.models import User 

class SenaryoAnalizi(models.Model):
    senaryo_adi = models.CharField(max_length=200)
    senaryo_metni = models.TextField()
    analiz_sonucu = models.TextField()
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return self.senaryo_adi
    
class SenaryoAnalizi(models.Model):
    """
    Kullanıcı tarafından girilen senaryo metnini ve Gemini'nin analiz sonuçlarını saklar.
    """
    senaryo_adi = models.CharField(max_length=255, blank=True, null=True, verbose_name="Senaryo Adı")
    
    senaryo_metni = models.TextField(verbose_name="Senaryo Metni")
    analiz_sonucu = models.TextField(verbose_name="Analiz Sonucu")
    olusturma_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")

    class Meta:
        verbose_name = "Senaryo Analizi"
        verbose_name_plural = "Senaryo Analizleri"
        ordering = ['-olusturma_tarihi'] # En yeni kayıtlar en üstte görünsün

    def __str__(self):
        # Admin panelinde ve başka yerlerde objeyi temsil etmek için kullanılır
        return self.senaryo_adi if self.senaryo_adi else f"Analiz - {self.olusturma_tarihi.strftime('%Y-%m-%d %H:%M')}"
# Create your models here.
