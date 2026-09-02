import json
import os
from dotenv import load_dotenv

# gizli anahtarları sisteme yükle
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse
from google import genai
from google.genai import types
app = FastAPI(
    title="Tinus Technologies Chatbot API",
    description="Sıkça Sorulan Sorular ve Akıllı Sohbet Robotu Backend Servisi",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client()

# HAFIZA: Oturumları geçici bellekte tutacağımız sözlük
chat_sessions = {}

def load_faqs():
    file_path = os.path.join(os.path.dirname(__file__), "faqs.json")
    if not os.path.exists(file_path):
        return {"categories": []}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

class QuestionRequest(BaseModel):
    session_id: str  # Frontend'den gelecek oturum kimliği
    query: str

@app.get("/", response_class=FileResponse, tags=["Chatbot UI"])
async def serve_frontend():
    html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "index.html")
    if not os.path.exists(html_path):
        raise HTTPException(status_code=404, detail="Arayüz dosyası (index.html) bulunamadı.")
    return FileResponse(html_path)

@app.get("/api/v1/categories", tags=["Chatbot"])
async def get_categories():
    data = load_faqs()
    categories = [{"category_id": c["category_id"], "category_name": c["category_name"]} for c in data.get("categories", [])]
    return {"categories": categories}

@app.post("/api/v1/ask", tags=["Chatbot"])
async def ask_question(request: QuestionRequest):
    try:
        # 1. Oturum yoksa yeni bir sohbet başlat ve SSS'i modele öğret
        if request.session_id not in chat_sessions:
            data = load_faqs()
            context_text = ""
            for category in data.get("categories", []):
                context_text += f"Kategori: {category.get('category_name')}\n"
                for faq in category.get("questions", []):
                    context_text += f"- Soru: {faq['question']}\n  Cevap: {faq['answer']}\n"
            
            sys_instruct = (
    "Sen Tinus Technologies'in akıllı destek asistanısın ve kullanıcıyla yaptığın geçmiş konuşmaları NET BİR ŞEKİLDE HATIRLIYORSUN. "
    "Kullanıcı 'sana az önce ne sordum?', 'önceki mesajım neydi?' gibi sohbetin geçmişiyle ilgili sorular sorarsa, hafızanı kullanarak doğrudan cevap ver. "
    "Bunun dışındaki şirket ve ürün soruları için sadece aşağıdaki SSS veritabanını kullan. Veritabanında olmayan konularda ekibe yönlendir.\n\n"
    f"Veritabanı:\n{context_text}"
)
            
            chat_sessions[request.session_id] = client.chats.create(
                model="gemini-2.0-flash",
                config=types.GenerateContentConfig(
                    system_instruction=sys_instruct
                )
            )

        # 2. İlgili oturumu al ve mesajı gönder
        chat = chat_sessions[request.session_id]
        response = chat.send_message(request.query)
        
        return {
            "matched": True,
            "answer": response.text,
            "category": "Google Gemini Destekli Yanıt"
        }
        
    except Exception as e:
        return {
            "matched": False,
            "answer": f"Yapay zeka servisine bağlanırken bir hata oluştu: {str(e)}",
            "redirect_contact": True
        }