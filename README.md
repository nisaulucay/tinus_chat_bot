# 🤖 Tinus Technologies - Akıllı Destek Asistanı

> Bu proje, **Tinus Technologies** staj çalışmaları kapsamında geliştirilen; kurumsal SSS (Sıkça Sorulan Sorular) veritabanını akıllı doğal dil işleme yetenekleriyle birleştiren, modern ve responsive arayüze sahip bir Yapay Zeka Destekli Destek Asistanı uygulamasıdır.

---

## 🚀 Proje Hakkında
Geleneksel anahtar kelime eşleştirmesine dayalı chatbot sistemlerinin sınırlılıklarını aşmak amacıyla geliştirilen bu sistem; FastAPI altyapısı, Google Gemini yapay zeka modelleri ve modern web teknolojilerini bir araya getirerek kullanıcılara akıcı, samimi ve kurumsal bir deneyim sunar.

---

## 🛠️ Kullanılan Teknolojiler ve Mimari

### **Backend (Sunucu Tarafı)**
* **Python 3.11+**
* **FastAPI:** Yüksek performanslı, asenkron RESTful API geliştirme çatı programı.
* **Uvicorn:** ASGI sunucu uygulaması.
* **Pydantic:** Veri doğrulama ve tip güvenliği.
* **Google GenAI SDK (`google-genai`):** Google Gemini entegrasyonu için resmi Python kütüphanesi.

### **Frontend (Arayüz Tarafı)**
* **HTML5 & Modern CSS3:** Kurumsal gradyan tasarımlar, esnek yerleşim (`Flexbox`) ve mobil uyumlu responsive yapı.
* **JavaScript (ES6+ & Fetch API):** Asenkron sunucu haberleşmesi, dinamik mesaj baloncukları ve "Asistan düşünüyor..." kullanıcı deneyimi (UX) optimizasyonu.

### **Veri Yönetimi & Dağıtım**
* **JSON Tabanlı Veritabanı (`faqs.json`):** Kurumsal kategorize edilmiş soru-cevap havuzu.
* **Cloud & Tunneling:** Yerel testler için `Localtunnel`, kesintisiz 7/24 bulut dağıtımı için **Render Cloud** platformu.

---

## 📂 Proje Dosya Yapısı


tinus-chatbot-backend/
│
├── app/
│   ├── __init__.py
│   └── main.py          # FastAPI ana sunucu ve Gemini AI entegrasyon mantığı
│
├── index.html           # Modern, responsive kullanıcı arayüzü
├── faqs.json            # Kurumsal SSS veritabanı
├── requirements.txt     # Python bağımlılıkları listesi
└── README.md            # Proje dokümantasyonu






⚙️ Kurulum ve Çalıştırma Rehberi
Projeyi yerel ortamınızda çalıştırmak için aşağıdaki adımları takip edebilirsiniz:

1. Depoyu Klonlayın

git clone [https://github.com/KULLANICI_ADIN/tinus-chatbot-backend.git](https://github.com/KULLANICI_ADIN/tinus-chatbot-backend.git)
cd tinus-chatbot-backend


2. Sanal Ortam (Virtual Environment) Oluşturun ve Aktifleştirin

python -m venv venv
# Windows için:
venv\Scripts\activate


3. Gerekli Kütüphaneleri Yükleyin

pip install -r requirements.txt


4. Çevre Değişkenlerini (API Key) Ayarlayın
Google AI Studio üzerinden aldığınız Gemini API anahtarınızı sistem ortam değişkeni olarak ekleyin veya main.py içerisindeki ilgili alana tanımlayın:


# Windows PowerShell için:
$env:GEMINI_API_KEY="senin_api_anahtarin"



5. Sunucuyu Başlatın

uvicorn app.main:app --reload --port 8001


## 🚀 Canlı Demo

Projenin 7/24 aktif olan canlı web servisine aşağıdaki bağlantıdan ulaşabilirsiniz:

- **Canlı Uygulama:** [Tinus Destek Asistanı](https://tinus-chat-bot.onrender.com)

<img width="955" height="748" alt="image" src="https://github.com/user-attachments/assets/12a0c0ff-24fb-4a04-99cb-efa6532e1ae5" />
<img width="1052" height="785" alt="Ekran görüntüsü 2026-09-01 141205" src="https://github.com/user-attachments/assets/fe1b74d8-4172-4cf8-8f55-578adbff7baf" />
<img width="930" height="729" alt="Ekran görüntüsü 2026-09-01 143053" src="https://github.com/user-attachments/assets/29eb5a92-873d-444f-b7a6-26f534d207df" />

