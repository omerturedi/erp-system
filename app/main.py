from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
from app.core.config import settings
from app.admin import create_admin

# FastAPI uygulaması
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="ERP Yönetim Sistemi",
    version="1.0.0"
)

# CORS ayarları
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Flask Admin uygulamasını oluştur
admin_app = create_admin()

# Flask uygulamasını FastAPI'ye monte et
app.mount("/admin", WSGIMiddleware(admin_app))
app.mount("/login", WSGIMiddleware(admin_app))

@app.get("/")
async def root():
    return {
        "message": "ERP Yönetim Sistemi'ne Hoş Geldiniz",
        "version": "1.0.0",
        "admin_url": "/admin"  # Admin panel URL'si
    }