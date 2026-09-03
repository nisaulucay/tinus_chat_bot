import time
import logging
import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse
from google import genai
from google.genai import types
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

# LOGGING YAPILANDIRMASI
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

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
        logging.warning("faqs.json dosyası bulunamadı!")
        return {"categories": []}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

class QuestionRequest(BaseModel):
    session_id: str
    query: str = Field(min_length=1, description="Kullanıcının sorusu boş olamaz")
    
class FeedbackRequest(BaseModel):
    liked: bool
    message: str

@app.get("/", response_class=FileResponse, tags=["Chatbot UI"], summary="Arayüzü Yükle", description="Kullanıcı arayüzünü (index.html) tarayıcıya sunar.")
async def serve_frontend():
    html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "index.html")
    if not os.path.exists(html_path):
        raise HTTPException(status_code=404, detail="Arayüz dosyası (index.html) bulunamadı.")
    return FileResponse(html_path)

@app.get("/api/v1/categories", tags=["Chatbot"], summary="Sık Sorulan Soru Kategorilerini Listele", description="Sistemde tanımlı olan tüm SSS kategori ID ve adlarını döner.")
async def get_categories():
    data = load_faqs()
    categories = [{"category_id": c["category_id"], "category_name": c["category_name"]} for c in data.get("categories", [])]
    return {"categories": categories}

@app.post("/api/v1/ask", tags=["Chatbot"], summary="Akıllı Asistana Soru Sor", description="Kullanıcıdan gelen oturum kimliği ve sorguyu alır, süre ölçümü yaparak Gemini AI ile yanıt üretir.")
async def ask_question(request: QuestionRequest):
    start_time = time.time()  # Kronometreyi başlat
    try:
        if request.session_id not in chat_sessions:
            logging.info(f"Yeni oturum oluşturuluyor. Session ID: {request.session_id}")
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
            
            chat_sessions[request.session_id] = client.chats.create(
                model="gemini-3.6-flash",
                config=types.GenerateContentConfig(
                    system_instruction=sys_instruct
                )
            )

        chat = chat_sessions[request.session_id]
        response = chat.send_message(request.query)
        
        end_time = time.time()  # Kronometreyi durdur
        elapsed_time = round(end_time - start_time, 2)  # Geçen süreyi saniye olarak hesapla
        
        logging.info(f"API Yanıt Süresi: {elapsed_time} saniye (Session: {request.session_id})")
        
        return {
            "matched": True,
            "answer": response.text,
            "category": "Google Gemini Destekli Yanıt",
            "response_time_seconds": elapsed_time
        }
        
    except Exception as e:
        end_time = time.time()
        elapsed_time = round(end_time - start_time, 2)
        logging.error(f"Yapay zeka servis hatası ({elapsed_time} saniyede başarısız oldu): {str(e)}")
        return {
            "matched": False,
            "answer": f"Yapay zeka servisine bağlanırken bir hata oluştu: {str(e)}",
            "redirect_contact": True
        }

@app.post("/api/v1/feedback", tags=["Chatbot"], summary="Kullanıcı Geri Bildirimi Al", description="Kullanıcıların yanıtlar için gönderdiği beğenme/beğenmeme durumunu kaydeder.")
async def receive_feedback(request: FeedbackRequest):
    if request.liked:
        logging.info("Geri bildirim: Kullanıcı bu mesajı beğendi 👍")
    else:
        logging.info("Geri bildirim: Kullanıcı bu mesajı beğenmedi 👎")
        
    return {"status": "success", "detail": "Geri bildiriminiz kaydedildi."}