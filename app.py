from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import requests
from transformers import pipeline
import json
import os

app = Flask(__name__)
CORS(app)

# Verileri saklamak için basit bir JSON dosyası kullanalım
DATA_FILE = "chatbot_data.json"

# Başlangıç verileri
DEFAULT_DATA = {
    "reminders": [],
    "preferences": {
        "default_city": "İstanbul",
        "theme": "light"
    }
}

# NLP modelini yükle
try:
    nlp_model = pipeline('question-answering', model='bert-base-turkish-128k-uncased')
except:
    nlp_model = None
    print("NLP modeli yüklenemedi, basit modda çalışıyor")

# Veri dosyasını yükleme
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return DEFAULT_DATA.copy()

# Veri dosyasını kaydetme
def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/chat', methods=['POST'])
def chat():
    data = load_data()
    user_input = request.json.get('message', '').lower().strip()
    response = {"response": "", "reminders": data["reminders"]}

    # 1. Günlük İşler
    if "hava durumu" in user_input:
        city = extract_city(user_input) or data["preferences"]["default_city"]
        weather = get_weather(city)
        response["response"] = weather
        response["weather"] = {
            "city": city,
            "temperature": extract_temperature(weather),
            "icon": get_weather_icon(weather)
        }
        
    elif any(keyword in user_input for keyword in ["saat kaç", "saat"]):
        current_time = datetime.datetime.now().strftime("%H:%M")
        response["response"] = f"⌚ Şu an saat {current_time}"
        response["time"] = current_time
        
    elif any(keyword in user_input for keyword in ["tarih", "günlerden ne"]):
        current_date = datetime.datetime.now().strftime("%d %B %Y, %A")
        response["response"] = f"📅 Bugün {current_date}"
        response["date"] = current_date
        
    elif "hatırlatıcı ekle" in user_input:
        reminder = user_input.replace("hatırlatıcı ekle", "").strip()
        if reminder:
            data["reminders"].append({
                "text": reminder,
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            save_data(data)
            response["response"] = f"🔔 Hatırlatıcı eklendi: '{reminder}'"
            response["reminders"] = data["reminders"]
        
    elif any(keyword in user_input for keyword in ["hatırlatıcılarım", "hatırlatıcılar"]):
        if data["reminders"]:
            reminders_text = "\n".join([f"• {r['text']} ({r['date']})" for r in data["reminders"]])
            response["response"] = f"📝 Hatırlatıcılarınız:\n{reminders_text}"
        else:
            response["response"] = "📝 Hiç hatırlatıcınız yok"
    
    # 2. Sistem Komutları
    elif "varsayılan şehir" in user_input:
        city = extract_city(user_input)
        if city:
            data["preferences"]["default_city"] = city
            save_data(data)
            response["response"] = f"🏙️ Varsayılan şehir '{city}' olarak ayarlandı"
    
    # 3. Soru-Cevap Sistemi
    else:
        response["response"] = handle_conversation(user_input, data)
    
    return jsonify(response)

def extract_city(text):
    # Metinden şehir ismini çıkarma
    city_keywords = ["hava durumu", "varsayılan şehir"]
    for keyword in city_keywords:
        if keyword in text:
            parts = text.split(keyword)
            if len(parts) > 1:
                city = parts[-1].strip()
                if city:
                    return city.title()
    return None

def extract_temperature(weather_text):
    # Hava durumu metninden sıcaklık bilgisini çıkarma
    try:
        return weather_text.split("sıcaklık:")[1].split("°C")[0].strip()
    except:
        return None

def get_weather_icon(weather_text):
    # Hava durumuna göre ikon belirleme
    if "güneş" in weather_text or "açık" in weather_text:
        return "☀️"
    elif "yağmur" in weather_text:
        return "🌧️"
    elif "bulut" in weather_text:
        return "⛅"
    elif "kar" in weather_text:
        return "❄️"
    return "🌡️"

def handle_conversation(question, data):
    # Önceden tanımlanmış bilgi tabanı
    knowledge_base = {
        "sen kimsin": "Ben günlük işlerinize yardımcı olan kişisel yapay zeka asistanınızım 🤖",
        "ne yapabilirsin": "Size hava durumu bilgisi verebilir, hatırlatıcı oluşturabilir, saat ve tarih söyleyebilirim. Ayrıca basit sorularınızı yanıtlayabilirim.",
        "nasılsın": "Ben bir programım ama sizin için her zaman hazırım! 😊",
        "teşekkür": "Rica ederim! Başka nasıl yardımcı olabilirim? 💙",
        "merhaba": "Merhaba! Size nasıl yardımcı olabilirim? 😊",
        "varsayılan şehir": f"Şu anki varsayılan şehir: {data['preferences']['default_city']}. Değiştirmek için 'varsayılan şehir İstanbul' gibi bir komut kullanabilirsiniz."
    }
    
    # Öncelikle basit soruları kontrol et
    for q, a in knowledge_base.items():
        if q in question:
            return a
    
    # NLP modeli ile yanıt üret
    if nlp_model:
        try:
            result = nlp_model({
                'question': question,
                'context': "Ben bir yardımcı chatbotum. Kullanıcılara günlük işlerinde yardım ediyorum."
            })
            if result['score'] > 0.3:
                return result['answer']
        except:
            pass
    
    return "Üzgünüm, bu konuda yeterli bilgim yok. Başka nasıl yardımcı olabilirim?"

def get_weather(city="İstanbul"):
    # API KEY'i buraya ekleyin (https://openweathermap.org/api)
    API_KEY = "YOUR_API_KEY"
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=tr"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            return f"{city.capitalize()} için hava durumu: {desc}, sıcaklık: {temp}°C"
        else:
            return f"Hava durumu bilgisi alınamadı. Lütfen şehir ismini kontrol edin."
    except Exception as e:
        print("Hava durumu hatası:", e)
        return "Hava durumu servisine bağlanılamadı. Lütfen daha sonra tekrar deneyin."

if __name__ == '__main__':
    # Veri dosyasını kontrol et
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_DATA, f, ensure_ascii=False, indent=2)
    
    app.run(debug=True, port=5000)