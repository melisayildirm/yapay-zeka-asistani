
import os
import google.generativeai as genai
from dotenv import load_dotenv
import pypdf
from django.shortcuts import render 

from .forms import SenaryoForm 
from .models import SenaryoAnalizi
import markdown 
import re

# .env dosyasından API anahtarını yükle
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

gemini_model = None 

if not API_KEY:
    # API anahtarı bulunamazsa terminale uyarı yazdır
    print("HATA: GOOGLE_API_KEY ortam değişkeni bulunamadı. Lütfen .env dosyanızı kontrol edin.")
else:
    try:
        # API anahtarıyla Gemini modelini yapılandır ve başlat
        genai.configure(api_key=API_KEY)
        gemini_model = genai.GenerativeModel('gemini-1.5-flash') 
    except Exception as e:
        # Model başlatılırken bir hata oluşursa terminale yazdır
        print(f"HATA: Gemini modeli oluşturulurken bir hata oluştu: {e}")
        print("Lütfen API anahtarınızın geçerliliğini ve internet bağlantınızı kontrol edin.")


def analiz_senaryo(request):
    analiz_sonucu = None
    hata_mesaji = None # Hata mesajlarını tutmak için
    original_senaryo_metni_preview = "" # Giriş metninin önizlemesini tutmak için

    if request.method == 'POST':
        form = SenaryoForm(request.POST, request.FILES) # request.FILES, dosya yüklemeleri için gerekli

        # Form geçerliyse işlemleri yap
        if form.is_valid():
            senaryo_metni_input = form.cleaned_data.get('senaryo_metni')
            pdf_dosyasi = form.cleaned_data.get('pdf_dosyasi')
            
            original_senaryo_tam_metni = "" # Analiz edilecek tam metni tutar

            # Metin alanı doluysa metni al
            if senaryo_metni_input:
                original_senaryo_tam_metni = senaryo_metni_input
            # PDF dosyası yüklendiyse PDF'den metni çıkar
            elif pdf_dosyasi:
                try:
                    # PyPDF ile PDF'ten metin çıkar
                    pdf_file_obj = pdf_dosyasi.file # Dosya objesine erişim
                    reader = pypdf.PdfReader(pdf_file_obj)
                    
                    print(f"PDF'deki sayfa sayısı: {len(reader.pages)}") # Hata ayıklama için

                    for page_num in range(len(reader.pages)):
                        page = reader.pages[page_num]
                        extracted_text = page.extract_text()
                        if extracted_text:
                            original_senaryo_tam_metni += extracted_text + "\n"
                        else:
                            print(f"Uyarı: Sayfa {page_num + 1} boş veya metin çıkarılamadı.")
                    
                    if not original_senaryo_tam_metni.strip():
                        hata_mesaji = "PDF dosyasından metin çıkarılamadı veya dosya boş. Taranmış bir PDF olabilir."
                        print("HATA: PDF'den metin çıkarılamadı.")

                except Exception as e:
                    # PDF işleme hatası yakalama
                    hata_mesaji = f"PDF dosyasını işlerken bir hata oluştu: {e}. Lütfen geçerli bir PDF dosyası yüklediğinizden emin olun."
                    print(f"PDF İşleme Hatası (views.py): {e}")
                    import traceback # Detaylı hata izi için
                    traceback.print_exc()
            
            # Hata mesajı yoksa ve metin varsa ve Gemini modeli hazırsa
            if not hata_mesaji and original_senaryo_tam_metni.strip() and gemini_model:
                # Gemini'ye gönderilecek prompt (istek)
             prompt = f"""Aşağıdaki senaryo için kapsamlı ve detaylandırılmış bir gereksinim analizi hazırla:

            1. Fonksiyonel Gereksinimler (FR): Her bir gereksinimi numaralandır, açıkla ve örneklerle destekle.
            2. Fonksiyonel Olmayan Gereksinimler (NFR): Başlık vermekle yetinme, neden gerekli olduklarını teknik ve mantıksal olarak açıkla.
            3. Kullanıcı Rolleri: Roller sadece isim olarak değil, sistemdeki görevleriyle birlikte tanımlansın.
            4. Kullanım Senaryoları:
            UC-ID:
                - Adım 1: ...
                - Adım 2: ...
                - Adım 3: ...
            5. Teknik Gereksinimler:
                Her teknik gereksinimi şu şekilde yaz:
                - Bileşen: [Örneğin OCR]
                - Açıklama: Ne işe yarıyor?
                - Öneri: Hangi araç/teknoloji kullanılabilir?
            6. İş Kuralları:
                - BR-ID: [Kural açıklaması]
                - Olası Sonuç: Ne gibi sorunlara yol açar?
            7. Veri Gereksinimleri:
                - [veri tipi 1]
                - [veri tipi 2]
                - ...

                 ---

            Cevabın yukarıdaki başlıklara uygun olarak detaylı ve madde madde olmalıdır. Uzun ama okunabilir şekilde yaz. Gereksiz tekrarlar veya format dışı açıklamalardan kaçın. Yanıtı sadece düz metin olarak döndür, tablo veya HTML istemiyorum.

            Senaryo:
            {original_senaryo_tam_metni}
            """


             try:
                    # Gemini API'sini çağır
                    gemini_response = gemini_model.generate_content(prompt)
                    
                    analiz_sonucu_raw = gemini_response.text # Ham yanıtı al
                    analiz_sonucu_html = markdown.markdown(analiz_sonucu_raw)
                    analiz_sonucu_html = re.sub(r'(?:<p>•\s*)(.+?)(?:</p>)', r'<ul><li>\1</li></ul>', analiz_sonucu_html)
                    analiz_sonucu_html = re.sub(r'<ol>\s*(.*?)\s*</ol>', lambda m: m.group(1).replace('<li>', '<p>').replace('</li>', '</p>'), flags=re.DOTALL)



                    # Analiz sonucunu veritabanına kaydet
                    try:
                        senaryo_obj = SenaryoAnalizi.objects.create(
                        
                            senaryo_adi=original_senaryo_tam_metni[:100], # Metnin ilk 100 karakterini ad olarak al
                            senaryo_metni=original_senaryo_tam_metni,
                            analiz_sonucu=analiz_sonucu_raw # Ham Markdown metni kaydet
                        )
                        print(f"Analiz veritabanına kaydedildi: ID - {senaryo_obj.id}")
                    except Exception as db_error:
                        hata_mesaji = f"Analiz veritabanına kaydedilirken bir hata oluştu: {db_error}"
                        print(f"Veritabanı Kaydetme Hatası: {db_error}")

                    analiz_sonucu = analiz_sonucu_html # Şablona HTML olarak gönder

             except Exception as e:
                    # Gemini API yanıt hatası yakalama
                    hata_mesaji = f"Gemini'den yanıt alınırken bir hata oluştu: {e}. Lütfen senaryo metninin çok uzun olmadığından veya API kotanızın dolmadığından emin olun."
                    print(f"Gemini API Hatası: {e}")
            elif not gemini_model:
                hata_mesaji = "Gemini modeli başlatılamadı. Lütfen API anahtarınızı kontrol edin."
           
            if not form.is_valid():
                hata_mesaji = form.errors
                print(f"Form Hataları: {form.errors}")

   
    else:
        form = SenaryoForm() # Boş bir form oluştur

   
    context = {
        'form': form,
        'analiz_sonucu': analiz_sonucu,
        'hata_mesaji': hata_mesaji,
        'original_senaryo_metni_preview': original_senaryo_metni_preview
     
    }
    return render(request, 'analiz_uygulamasi/analiz.html', context)
