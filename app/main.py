import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse
from google import genai

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

# Yeni Google GenAI İstemcisi
client = genai.Client()

def load_faqs():
    file_path = os.path.join(os.path.dirname(__file__), "faqs.json")
    if not os.path.exists(file_path):
        return {"categories": []}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

class QuestionRequest(BaseModel):
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
    data = load_faqs()
    
    context_text = ""
    for category in data.get("categories", []):
        context_text += f"Kategori: {category.get('category_name')}\n"
        for faq in category.get("questions", []):
            context_text += f"- Soru: {faq['question']}\n  Cevap: {faq['answer']}\n"

    prompt = f"""
    Sen Tinus Technologies'in akıllı destek asistanısın. Kullanıcıların selamlaşmalarına (merhaba, nasılsın vb.) kibarca karşılık ver. 
    Aşağıdaki kurumsal SSS veritabanını referans alarak soruları doğal, akıcı ve samimi bir Türkçe ile yanıtla. 
    Eğer bilgi veritabanında yoksa, kullanıcıyı profesyonelce Tinus Technologies ekibiyle iletişime geçmeye yönlendir.

    Veritabanı:
    {context_text}

    Kullanıcı Sorusu: {request.query}
    """

    try:
        response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt,
)
        answer = response.text
        return {
            "matched": True,
            "answer": answer,
            "category": "Google Gemini Destekli Yanıt"
        }
        
    except Exception as e:
        return {
            "matched": False,
            "answer": f"Yapay zeka servisine bağlanırken bir hata oluştu: {str(e)}",
            "redirect_contact": True
        }