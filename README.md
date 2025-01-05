# ERP Yönetim Sistemi

Bu proje, çok seviyeli yetkilendirme sistemi içeren bir ERP yönetim sistemidir.

## Özellikler

- Üç seviyeli yetkilendirme (Super Admin, Master Admin, Admin)
- Modül bazlı yetkilendirme
- Şirket bazlı veri izolasyonu
- Audit logging sistemi

## Kurulum

1. Python 3.9+ yüklü olmalıdır
2. PostgreSQL veritabanı kurulu olmalıdır

```bash
# Sanal ortam oluştur
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
.\venv\Scripts\activate  # Windows

# Gereksinimleri yükle
pip install -r requirements.txt

# Veritabanını oluştur
createdb erp_system

# Migration'ları çalıştır
alembic upgrade head

# Uygulamayı başlat
uvicorn app.main:app --reload
```

## API Dokümantasyonu

API dokümantasyonuna aşağıdaki URL'lerden erişebilirsiniz:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Yetkilendirme Seviyeleri

1. **Super Admin**
   - Tüm sistem üzerinde tam yetki
   - Modül oluşturma/düzenleme/silme
   - Master Admin yönetimi

2. **Master Admin**
   - Kendisine atanmış modülleri görüntüleme
   - Kendi şirketindeki Admin'leri yönetme
   - Admin'lere modül yetkisi verme/kaldırma

3. **Admin**
   - Kendisine atanmış aktif modüllere erişim
   - Master Admin tarafından belirlenen yetkilere sahip 