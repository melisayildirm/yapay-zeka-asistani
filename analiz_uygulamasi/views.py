import os
import google.generativeai as genai
from dotenv import load_dotenv
import pypdf
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from .forms import SenaryoForm
from .models import SenaryoAnalizi  # <-- SenaryoAnalizi modelini import ediyoruz
import markdown # Markdown kütüphanesi



load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

gemini_model = None

if not API_KEY:
    print("HATA: GOOGLE_API_KEY ortam değişkeni bulunamadı. Lütfen .env dosyanızı kontrol edin.")
else:
    genai.configure(api_key=API_KEY)
    MODEL_NAME = "models/gemini-1.5-flash-latest"

    try:
        gemini_model = genai.GenerativeModel(MODEL_NAME)
    except Exception as e:
        print(f"HATA: Gemini modeli oluşturulurken bir hata oluştu: {e}")
        print("Lütfen MODEL_NAME değerini ve API anahtarınızın geçerliliğini kontrol edin.")


# --- Görünüm (View) Fonksiyonu ---
def analiz_senaryo(request):
    analiz_sonucu = None
    hata_mesaji = None
    original_senaryo_metni_preview = ""

    if request.method == 'POST':
        form = SenaryoForm(request.POST, request.FILES)
        if form.is_valid():
            senaryo_metni_input = form.cleaned_data.get('senaryo_metni')
            pdf_dosyasi = form.cleaned_data.get('pdf_dosyasi')
            
            original_senaryo_tam_metni = ""

            if senaryo_metni_input:
                original_senaryo_tam_metni = senaryo_metni_input
            elif pdf_dosyasi:
                try:
                    reader = pypdf.PdfReader(pdf_dosyasi)
                    for page_num in range(len(reader.pages)):
                        page = reader.pages[page_num]
                        original_senaryo_tam_metni += page.extract_text() + "\n"
                    
                    if not original_senaryo_tam_metni.strip():
                        hata_mesaji = "PDF dosyasından metin çıkarılamadı veya dosya boş. Taranmış bir PDF olabilir."
                except Exception as e:
                    hata_mesaji = f"PDF dosyasını işlerken bir hata oluştu: {e}"

            if original_senaryo_tam_metni:
                original_senaryo_metni_preview = original_senaryo_tam_metni[:500] + ("..." if len(original_senaryo_tam_metni) > 500 else "")

            if not hata_mesaji and original_senaryo_tam_metni.strip() and gemini_model:
                prompt = f"""Aşağıdaki senaryo için temel fonksiyonel (FR) ve fonksiyonel olmayan (NFR) gereksinimleri madde madde listeler misin? Her bir gereksinimin FR veya NFR olduğunu belirt. Ayrıca, bu senaryoda yer alabilecek potansiyel kullanıcı rollerini ve bu senaryoyu gerçekleştirmek için gerekli olabilecek temel teknik gereksinimleri (kullanılacak teknolojiler, altyapı vb.) de kısa ve öz bir şekilde belirt.

Senaryo Metni:
{original_senaryo_tam_metni}
"""
                try:
                    gemini_response = gemini_model.generate_content(prompt)
                    
                    # Gemini'nin Markdown yanıtını HTML'e dönüştür
                    analiz_sonucu_html = markdown.markdown(gemini_response.text) # HTML olarak sunmak için
                    analiz_sonucu_raw = gemini_response.text # Veritabanına kaydetmek için ham metin

                    # Analiz sonucunu veritabanına kaydet
                    try:
                        senaryo_obj = SenaryoAnalizi.objects.create(
                            senaryo_adi=original_senaryo_tam_metni[:100], # İlk 100 karakteri senaryo adı yap
                            senaryo_metni=original_senaryo_tam_metni,
                            analiz_sonucu=analiz_sonucu_raw # Ham Markdown metni kaydet
                        )
                        print(f"Analiz veritabanına kaydedildi: ID - {senaryo_obj.id}")
                    except Exception as db_error:
                        hata_mesaji = f"Analiz veritabanına kaydedilirken bir hata oluştu: {db_error}"
                        print(f"Veritabanı Kaydetme Hatası: {db_error}")

                    analiz_sonucu = analiz_sonucu_html # Şablona HTML olarak gönder

                except Exception as e:
                    hata_mesaji = f"Gemini'den yanıt alınırken bir hata oluştu: {e}. Lütfen senaryo metninin çok uzun olmadığından veya API kotanızın dolmadığından emin olun."
            elif not gemini_model:
                hata_mesaji = "Gemini modeli başlatılamadı. Lütfen API anahtarınızı kontrol edin."
        else:
            hata_mesaji = form.errors
            print(f"Form Hataları: {form.errors}")

    else:
        form = SenaryoForm()

    context = {
        'form': form,
        'analiz_sonucu': analiz_sonucu, # Bu artık HTML formatında olacak
        'hata_mesaji': hata_mesaji,
        'original_senaryo_metni_preview': original_senaryo_metni_preview
    }
    return render(request, 'analiz_uygulamasi/analiz.html', context)