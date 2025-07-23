

from django.contrib import admin
from .models import SenaryoAnalizi


@admin.register(SenaryoAnalizi)
class SenaryoAnaliziAdmin(admin.ModelAdmin):
    list_display = ('senaryo_adi', 'olusturma_tarihi') 
    list_filter = ('olusturma_tarihi',) 
    search_fields = ('senaryo_adi', 'senaryo_metni', 'analiz_sonucu')
