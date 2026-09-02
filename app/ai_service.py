import os
import json
import logging
from google import genai
from google.genai import types

client = genai.Client()

# Oturumları ve hafızayı tutacağımız sözlük
chat_sessions = {}

def load_faqs():
    file_path = os.path.join(os.path.dirname(__file__), "faqs.json")
    if not os.path.exists(file_path):
        alt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "faqs.json")
        if not os.path.exists(alt_path):
            logging.warning("faqs.json dosyası bulunamadı!")
            return {"categories": []}
        file_path = alt_path
        
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_ai_response(session_id: str, query: str):
    # Oturum yoksa yeni sohbet başlat ve SSS bağlamını yükle
    if session_id not in chat_sessions:
        logging.info(f"Yeni oturum oluşturuluyor. Session ID: {session_id}")
        data = load_faqs()
        context_text = ""
        for category in data.get("categories", []):
            context_text += f"Kategori: {category.get('category_name')}\n"
            for faq in category.get("questions", []):
                context_text += f"- Soru: {faq['question']}\n  Cevap: {faq['answer']}\n"
        
        sys_instruct = (
            "Sen Tinus Technologies'in akıllı destek asistanısın ve kullanıcıyla yaptığın geçmiş konuşmaları NET BİR ŞEKİLDE HATIRLIYORSUN. "
            "Kullanıcı 'sana az önce ne sordum?', 'önceki mesajım neydi?' gibi sohbetin geçmişiyle ilgili sorular sorarsa, hafızanı kullanarak doğrudan cevap ver. "
            "Eğer soruyu veya isteği anlamazsan, kullanıcıdan konuyu veya soruyu kibarca tekrar etmesini iste. "
            "Bunun dışındaki şirket ve ürün soruları için sadece aşağıdaki SSS veritabanını kullan. Veritabanında olmayan konularda ekibe yönlendir.\n\n"
            f"Veritabanı:\n{context_text}"
        )
        
        chat_sessions[session_id] = client.chats.create(
            model="gemini-3.6-flash",
            config=types.GenerateContentConfig(
                system_instruction=sys_instruct
            )
        )

    # İlgili oturum üzerinden mesajı gönder
    chat = chat_sessions[session_id]
    response = chat.send_message(query)
    return response.text