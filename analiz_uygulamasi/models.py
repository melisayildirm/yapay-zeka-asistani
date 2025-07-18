from django.db import models
# analiz_uygulamasi/models.py

from django.db import models

class SenaryoAnalizi(models.Model):
    """
    Kullanıcı tarafından girilen senaryo metnini ve Gemini'nin analiz sonuçlarını saklar.
    """
    senaryo_adi = models.CharField(max_length=255, blank=True, null=True, verbose_name="Senaryo Adı")
    # Kullanıcının girdiği/PDF'ten okunan orijinal senaryo metni
    senaryo_metni = models.TextField(verbose_name="Senaryo Metni")
    # Gemini'den gelen analiz metni (FR, NFR, Roller, Teknikler hepsi bir arada)
    analiz_sonucu = models.TextField(verbose_name="Analiz Sonucu")
    # Analizin yapıldığı tarih ve saat
    olusturma_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    # olusturan_kullanici = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) # İsterseniz daha sonra kullanıcı modelini bağlayabilirsiniz

    class Meta:
        verbose_name = "Senaryo Analizi"
        verbose_name_plural = "Senaryo Analizleri"
        ordering = ['-olusturma_tarihi'] # En yeni kayıtlar en üstte görünsün

    def __str__(self):
        # Admin panelinde ve başka yerlerde objeyi temsil etmek için kullanılır
        return self.senaryo_adi if self.senaryo_adi else f"Analiz - {self.olusturma_tarihi.strftime('%Y-%m-%d %H:%M')}"
# Create your models here.
