import os
import google.generativeai as genai
from dotenv import load_dotenv
import pypdf
from django.shortcuts import render
from django.http import HttpResponse # Bu import ileride indirme özelliği için kullanılabilir
from django import forms # Forms modülünü import ediyoruz
from .forms import SenaryoForm # Kendi oluşturduğumuz SenaryoForm'u import ediyoruz

# --- AI Yapılandırması ---
# Uygulama başladığında bir kez yüklenir, her istekte tekrar çalışmaz.
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

gemini_model = None # Gemini model nesnesini tutacak değişken

if not API_KEY:
    print("HATA: GOOGLE_API_KEY ortam değişkeni bulunamadı. Lütfen .env dosyanızı kontrol edin.")
    # Production ortamında bu şekilde sadece print bırakılmaz, loglama yapılır.
else:
    genai.configure(api_key=API_KEY)
    MODEL_NAME = "models/gemini-1.5-flash-latest" # Kullanılacak Gemini modeli

    try:
        gemini_model = genai.GenerativeModel(MODEL_NAME)
    except Exception as e:
        print(f"HATA: Gemini modeli oluşturulurken bir hata oluştu: {e}")
        print("Lütfen MODEL_NAME değerini ve API anahtarınızın geçerliliğini kontrol edin.")

def analiz_senaryo(request):
    analiz_sonucu = None
    hata_mesaji = None   
    original_senaryo_metni_preview = "" 

    if request.method == 'POST':
        # Formu gelen verilerle (hem metin hem de dosya) oluşturur
        form = SenaryoForm(request.POST, request.FILES)

        if form.is_valid():
            senaryo_metni_input = form.cleaned_data.get('senaryo_metni') # Formdan metin alanını alır
            pdf_dosyasi = form.cleaned_data.get('pdf_dosyasi') # Formdan PDF dosyasını alır
            
            original_senaryo_tam_metni = "" # Gemini'ye gönderilecek senaryonun tam metni

            # Eğer kullanıcı metin girdiyse
            if senaryo_metni_input:
                original_senaryo_tam_metni = senaryo_metni_input
    
            elif pdf_dosyasi:
                try:
                   
                    reader = pypdf.PdfReader(pdf_dosyasi)
                    for page_num in range(len(reader.pages)):
                        page = reader.pages[page_num]
                        original_senaryo_tam_metni += page.extract_text() + "\n"
                    
                    # Eğer PDF'ten metin çıkarılamadıysa uyarı ver
                    if not original_senaryo_tam_metni.strip():
                        hata_mesaji = "PDF dosyasından metin çıkarılamadı veya dosya boş. Taranmış bir PDF olabilir."
                except Exception as e:
                    # PDF okuma sırasında oluşan hataları yakalar
                    hata_mesaji = f"PDF dosyasını işlerken bir hata oluştu: {e}"

            # Orijinal senaryo metninin ilk 500 karakterini önizleme için hazırlar
            if original_senaryo_tam_metni:
                original_senaryo_metni_preview = original_senaryo_tam_metni[:500] + ("..." if len(original_senaryo_tam_metni) > 500 else "")

            # Hata yoksa, senaryo metni boş değilse ve Gemini modeli başlatıldıysa
            if not hata_mesaji and original_senaryo_tam_metni.strip() and gemini_model:
                # Gemini'ye gönderilecek prompt (talimat) metnini oluşturur
                prompt = f"""Aşağıdaki senaryo için temel fonksiyonel (FR) ve fonksiyonel olmayan (NFR) gereksinimleri madde madde listeler misin? Her bir gereksinimin FR veya NFR olduğunu belirt. Ayrıca, bu senaryoda yer alabilecek potansiyel kullanıcı rollerini ve bu senaryoyu gerçekleştirmek için gerekli olabilecek temel teknik gereksinimleri (kullanılacak teknolojiler, altyapı vb.) de kısa ve öz bir şekilde belirt.

Senaryo Metni:
{original_senaryo_tam_metni}
"""
                try:
                    # Gemini modeline isteği gönderir ve yanıtı alır
                    gemini_response = gemini_model.generate_content(prompt)
                    analiz_sonucu = gemini_response.text # Yanıtın metin kısmını alır
                    
                except Exception as e:
                    hata_mesaji = f"Gemini'den yanıt alınırken bir hata oluştu: {e}. Lütfen senaryo metninin çok uzun olmadığından veya API kotanızın dolmadığından emin olun."
            # Eğer Gemini modeli başlatılamadıysa
            elif not gemini_model:
                hata_mesaji = "Gemini modeli başlatılamadı. Lütfen API anahtarınızı kontrol edin."
        else: 
            hata_mesaji = form.errors 
            print(f"Form Hataları: {form.errors}") 

    else:
        form = SenaryoForm() # Boş bir form örneği oluşturur (sayfa ilk yüklendiğinde)

    # HTML şablonuna gönderilecek verileri (context) hazırlar
    context = {
        'form': form, # HTML formunu oluşturmak için kullanılan Django Form nesnesi
        'analiz_sonucu': analiz_sonucu, # Gemini'den gelen analiz sonucu metni
        'hata_mesaji': hata_mesaji, # Kullanıcıya gösterilecek hata mesajı
        'original_senaryo_metni_preview': original_senaryo_metni_preview # Orijinal metnin kısa önizlemesi
    }
   
    return render(request, 'analiz_uygulamasi/analiz.html', context)

