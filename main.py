import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import pypdf  # PDF okumak için gerekli kütüphane

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    print("HATA: GOOGLE_API_KEY ortam değişkeni bulunamadı. .env dosyanızı kontrol edin.")
    exit()

genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-pro"
try:
    model = genai.GenerativeModel(MODEL_NAME)
except Exception as e:
    print(f"Model oluşturulurken hata oluştu: {e}")
    exit()

senaryo_metni = ""
print("\n--- Senaryo Giriş Seçimi ---")
print("1. Metin gir")
print("2. PDF'den al")
secim_tipi = input("Seçim (1/2): ")

if secim_tipi == '1':
    senaryo_metni = input("Senaryo: ")
    if not senaryo_metni.strip():
        print("Lütfen geçerli metin giriniz.")
        exit()
elif secim_tipi == '2':
    pdf_file_path = input("PDF dosya yolu: ")
    try:
        with open(pdf_file_path, 'rb') as file:
            reader = pypdf.PdfReader(file)
            for page in reader.pages:
                senaryo_metni += page.extract_text() + "\n"
        if not senaryo_metni.strip():
            print("PDF boş olabilir. OCR lazım olabilir.")
            exit()
    except Exception as e:
        print(f"PDF hatası: {e}")
        exit()
else:
    print("Geçersiz seçim.")
    exit()


prompt = f"""
Aşağıda yer alan sistem tanımını ve senaryosunu incele. Bu sistem için detaylı ve yapılandırılmış bir yazılım gereksinim analizi üret.

Çıktıyı JSON formatında döndür. Aşağıdaki şemaya birebir uy. Her alan, örneklerle dolu, açıklayıcı ve teknik anlamda anlamlı olmalı.

JSON yapısı:

{
  "proje_adi": "...",
  "giris": {
    "amac": "...",
    "kapsam": "..."
  },
  "kullanici_rolleri": [
    {
      "rol": "...",
      "gorevler": [
        "..."
      ]
    }
  ],
  "fonksiyonel_gereksinimler": {
    "FR-01": "...",
    "FR-02": "...",
    "...": "..."
  },
  "fonksiyonel_olmayan_gereksinimler": {
    "NFR-01": "...",
    "NFR-02": "...",
    "...": "..."
  },
  "kullanim_senaryolari": [
    {
      "id": "UC-01",
      "adimlar": [
        "..."
      ]
    }
  ],
  "is_kurallari": {
    "BR-01": "...",
    "BR-02": "...",
    "...": "..."
  },
  "veri_gereksinimleri": {
    "tahmini_veri_kumesi": [
      "..."
    ]
  },
  "sistem_gereksinimleri": {
    "...": "..."
  }
}

Lütfen alan isimlerini değiştirme. İçerikleri senaryoya göre üret. Klişe doldurmaktan kaçın. Sistemle ilgili özel detaylar ver.

Senaryo:
{senaryo_metni}
"""



print("\n💬 ReqAI'ye gönderilen istek:")

print("\n📥 Analiz sonucu alınıyor...\n")
try:
    gemini_response = model.generate_content(prompt)
    print(gemini_response.text)

    output_filename = "senaryo_analizi.txt"
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(gemini_response.text)
    print(f"\n✅ Analiz çıktısı '{output_filename}' dosyasına kaydedildi.")

except Exception as e:
    print(f"⚠️ Gemini yanıt hatası: {e}")

