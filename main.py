import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import pypdf # PDF okumak için gerekli kütüphane

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    print("HATA: GOOGLE_API_KEY ortam değişkeni bulunamadı. .env dosyanızı kontrol edin.")
    print("API anahtarınızın doğru olduğundan ve .env dosyasının main.py ile aynı dizinde olduğundan emin olun.")
    exit()

genai.configure(api_key=API_KEY)

MODEL_NAME = "models/gemini-1.5-flash-latest" # Kullanılan Gemini modeli

try:
    model = genai.GenerativeModel(MODEL_NAME)
except Exception as e:
    print(f"Model oluşturulurken bir hata oluştu: {e}")
    print("Lütfen MODEL_NAME değerini ve API anahtarınızın geçerliliğini kontrol edin.")
    exit()

# Buradan itibaren kullanıcıya giriş yöntemi seçeneği sunuluyor
senaryo_metni = "" # Senaryo metnini tutacak değişken

print("\n--- Senaryo Giriş Yöntemi Seçimi ---")
print("Senaryo metnini nasıl girmek istersiniz?")
print("1. Doğrudan metin olarak girmek istiyorum.")
print("2. Bir PDF dosyasından okunsun istiyorum.")

secim_tipi = input("Lütfen seçiminizi yapın (1 veya 2): ")

if secim_tipi == '1':
    print("\n--- Kendi Senaryonuzu Metin Olarak Girin ---")
    print("Lütfen analiz etmek istediğiniz senaryo metnini tek satırda girin ve Enter'a basın:")
    senaryo_metni = input("Senaryo: ")
    if not senaryo_metni.strip():
        print("Senaryo metni boş bırakılamaz. Program sonlandırılıyor.")
        exit()

elif secim_tipi == '2':
    print("\n--- PDF Dosyasından Senaryo Analizi ---")
    pdf_file_path = input("Lütfen analiz etmek istediğiniz PDF dosyasının yolunu girin (örn: C:\\Users\\...\senaryo.pdf): ")

    if not pdf_file_path.strip():
        print("PDF dosya yolu boş bırakılamaz. Program sonlandırılıyor.")
        exit()

    try:
        with open(pdf_file_path, 'rb') as file: # PDF dosyasını ikili modda okumak için
            reader = pypdf.PdfReader(file)
            # Her sayfadan metni çıkar ve senaryo_metni'ne ekle
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                senaryo_metni += page.extract_text() + "\n"
        
        if not senaryo_metni.strip():
            print("PDF dosyasından metin çıkarılamadı veya dosya boş. Taramalı bir PDF olabilir veya içerik bulunmuyor.")
            print("Eğer taramalı PDF ise, OCR (Optik Karakter Tanıma) kullanmanız gerekebilir.")
            exit()

    except FileNotFoundError:
        print(f"HATA: '{pdf_file_path}' yolu bulunamadı. Lütfen dosya yolunu kontrol edin.")
        exit()
    except Exception as e:
        print(f"PDF dosyasını işlerken bir hata oluştu: {e}")
        exit()
else:
    print("Geçersiz seçim. Lütfen 1 veya 2 girin. Program sonlandırılıyor.")
    exit()

# Analiz edilecek senaryo metninin ilk 500 karakterini ekrana yazdır 
print(f"\nAnaliz edilecek senaryo metni (ilk 500 karakter):\n{senaryo_metni[:500]}...")

# Gemini'ye gönderilecek prompt (talimat) oluşturuluyor
prompt = f"""Aşağıdaki senaryo için temel fonksiyonel (FR) ve fonksiyonel olmayan (NFR) gereksinimleri madde madde listeler misin? Her bir gereksinimin FR veya NFR olduğunu belirt. Ayrıca, bu senaryoda yer alabilecek potansiyel kullanıcı rollerini ve bu senaryoyu gerçekleştirmek için gerekli olabilecek temel teknik gereksinimleri (kullanılacak teknolojiler, altyapı vb.) de kısa ve öz bir şekilde belirt.

Senaryo Metni:
{senaryo_metni}
"""
print(f"\n Gemini'ye gönderilen istek: ")
# İsteğin tamamını görmek isterseniz aşağıdaki satırın başındaki hashtag'i kaldırın:
# print(prompt)

print("\n--Gemini'den Gelen Senaryo Analizi---")
try:
    gemini_response = model.generate_content(prompt)
    print(gemini_response.text)
    output_filename = "senaryo_analizi.txt"
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(gemini_response.text)
        print(f"\nAnaliz çıktısı '{output_filename}' dosyasına kaydedildi.")
    except Exception as file_error:
        print(f"HATA: Analiz çıktısı dosyaya kaydedilemedi: {file_error}")
except Exception as e:
    print(f"Gemini'den yanıt alınırken bir hata oluştu :{e}")
print("\n---------------------------------")