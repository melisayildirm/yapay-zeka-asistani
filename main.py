import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    print("HATA: GOOGLE_API_KEY ortam değişkeni bulunamadı. .env dosyanızı kontrol edin.")
    print("API anahtarınızın doğru olduğundan ve .env dosyasının main.py ile aynı dizinde olduğundan emin olun.")
    exit()

genai.configure(api_key=API_KEY)

MODEL_NAME = "models/gemini-1.5-flash-latest" 

try: 
    model = genai.GenerativeModel(MODEL_NAME)
except Exception as e:
    print(f"Model oluşturulurken bir hata oluştu: {e}")
    print("Lütfen MODEL_NAME değerini ve API anahtarınızın geçerliliğini kontrol edin.")
    exit() 
#  test_prompt = "Merhaba, ben bir LLM asistanı projesi geliştiriyorum. Kısaca kendini tanıtır mısın?"
#   test_response = model.generate_content(test_prompt)
#   print("\nAPI Bağlantısı Başarılı! Gemini'nin Test Yanıtı:")
#   print(test_response.text)
#  print("\n--------------------------------------------------")

   # data = []
   # try:
   #    with open('proje_veri.json', 'r', encoding='utf-8') as f:
   #        data = json.load(f)
   #    print(f"'{len(data)}' adet senaryo verisi başarıyla yüklendi.")
   # except FileNotFoundError:
   #    print("HATA: 'proje_veri.json' dosyası bulunamadı. Dosyanın main.py ile aynı klasörde olduğundan emin olun.")
   #    exit()
   # except json.JSONDecodeError as e:
    #    print(f"HATA: 'proje_veri.json' dosyası bozuk veya geçersiz JSON formatında. Detay: {e}")
    #    exit()

    #if data:
    #    print(f"Yüklenen ilk senaryo adı: {data[0]['senaryo_adi']}")
print("\n--- Kendi Senaryonuzu Girin---")
print("Litfen analiz etmek istediğiniz senaryo metninin girin ve Enter'a basın: ")

senaryo_metni=input("Senaryo: ")

if not senaryo_metni.strip():
    print("Senaryo metni boş bırakılamaz.Program sonlandırılıyor..")
    exit()

print(f"\nAnaliz edilecek senaryo metni:\n{senaryo_metni}")

prompt = f"""Aşağıdaki senaryo için temel fonksiyonel (FR) ve fonksiyonel olmayan (NFR) gereksinimleri madde madde listeler misin? Her bir gereksinimin FR veya NFR olduğunu belirt. Ayrıca, bu senaryoda yer alabilecek potansiyel kullanıcı rollerini ve bu senaryoyu gerçekleştirmek için gerekli olabilecek temel teknik gereksinimleri (kullanılacak teknolojiler, altyapı vb.) de kısa ve öz bir şekilde belirt.

Senaryo Metni:
{senaryo_metni}
"""
print(f"\n Gemini'ye gönderilen istek: ")
print(prompt)

print("\n--Gemini'den Gelen Senaryo Analizi---")
try:
    gemini_response=model.generate_content(prompt)
    print(gemini_response.text)
except Exception as e :
    print(f"Gemini'den yanıt alınırken bir hata oluştu :{e}")
    print("\n---------------------------------")