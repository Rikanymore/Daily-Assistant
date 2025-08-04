# GünlükAsistan 🤖

GünlükAsistan, günlük işlerinizi kolaylaştırmak için tasarlanmış Türkçe destekli akıllı bir chatbot uygulamasıdır. Hava durumu, saat, tarih bilgisi, hatırlatıcı yönetimi gibi temel özelliklerin yanı sıra BERT tabanlı doğal dil işleme yetenekleriyle kullanıcı sorularını yanıtlar.

## Özellikler ✨

- 🌦️ Şehir bazlı hava durumu bilgisi
- ⏰ Gerçek zamanlı saat ve tarih bilgisi
- 🔔 Hatırlatıcı ekleme ve yönetme
- 🏙️ Varsayılan şehir ayarlama
- 💬 Doğal dil işleme ile soru-cevap desteği
- 📁 Basit JSON tabanlı veri depolama
- 🔄 Flask tabanlı RESTful API

## Teknoloji Yığını 🛠️

- **Backend:** Python, Flask
- **NLP Modeli:** Hugging Face Transformers (bert-base-turkish-128k-uncased)
- **API:** OpenWeatherMap
- **Frontend:** HTML, CSS, JavaScript
- **Veri Depolama:** JSON

## Kurulum 🚀

### Önkoşullar
- Python 3.7+
- pip paket yöneticisi

### Adımlar

1. Depoyu klonlayın:

git clone https://github.com/sizin-kullanici-adiniz/GunlukAsistan.git
cd GunlukAsistan
 
2. Sanal ortam oluşturun ve etkinleştirin:

python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows

3. Gerekli paketleri yükleyin:

bash
pip install -r requirements.txt

4. OpenWeatherMap API anahtarınızı alın:

OpenWeatherMap adresinden ücretsiz API anahtarı alın

app.py dosyasında API_KEY = "YOUR_API_KEY" satırını kendi anahtarınızla güncelleyin

5. Uygulamayı başlatın:

python app.py

6. Tarayıcınızda http://localhost:5000 adresine gidin (link açmıyorsa f1+live server ile index dosyasını çalıştırın.)

Kullanım Kılavuzu 📖

Temel Komutlar:

Hava durumu: "İstanbul hava durumu" veya "hava durumu"

Saat bilgisi: "saat kaç"

Tarih bilgisi: "bugün günlerden ne", "tarih ne"

Hatırlatıcı ekle: "hatırlatıcı ekle yarın toplantı var"

Hatırlatıcıları listele: "hatırlatıcılarım", "hatırlatıcılar"

Varsayılan şehir değiştir: "varsayılan şehir Ankara"

NLP Örnekleri:

"Sen kimsin?"

"Ne yapabilirsin?"

"Nasılsın?"

"Teşekkür ederim"

"Merhaba"

Dosya Yapısı 📂

GunlukAsistan/
├── app.py                 # Ana Flask uygulaması
├── templates/             # HTML şablonları
│   └── index.html         # Ana arayüz dosyası
├── chatbot_data.json      # Kullanıcı verileri (uygulama çalıştığında oluşur)
├── requirements.txt       # Bağımlılıklar
├── .gitignore             # Git ignore dosyası
└── README.md              # Bu dosya