from django.contrib import admin
from django.contrib import admin
from .models import SenaryoAnalizi # models.py dosyasından SenaryoAnalizi modelini içe aktarıyoruz

@admin.register(SenaryoAnalizi) # Bu decorator, SenaryoAnalizi modelini admin paneline kaydeder
class SenaryoAnaliziAdmin(admin.ModelAdmin):
    # Admin panelindeki listeleme sayfasında hangi sütunların görüneceğini belirleriz
    list_display = ('senaryo_adi', 'olusturma_tarihi')
    # Admin panelinde arama kutusuna yazılarak aranabilecek alanları belirleriz
    search_fields = ('senaryo_adi', 'senaryo_metni')
    # Admin panelinde filtreleme çubuğunda görünecek alanları belirleriz
    list_filter = ('olusturma_tarihi',)
    # Admin panelindeki formda hangi alanların sırasıyla gösterileceğini belirleriz
    # fields = ('senaryo_adi', 'senaryo_metni', 'analiz_sonucu')
# Register your models here.
