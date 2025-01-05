from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash
from app.db.session import SessionLocal
from app.models.user import User, Role

def create_super_admin():
    db = SessionLocal()
    try:
        # Super Admin rolünü oluştur
        super_admin_role = Role(
            name="SUPER_ADMIN",
            description="Sistem yöneticisi"
        )
        db.add(super_admin_role)
        db.commit()
        db.refresh(super_admin_role)

        # Super Admin kullanıcısını oluştur
        super_admin = User(
            email="admin@example.com",
            username="superadmin",
            hashed_password=generate_password_hash("admin123"),
            is_active=True,
            role_id=super_admin_role.id
        )
        db.add(super_admin)
        db.commit()
        
        print("Super Admin başarıyla oluşturuldu!")
        print("E-posta: admin@example.com")
        print("Şifre: admin123")
    
    except Exception as e:
        print(f"Hata oluştu: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_super_admin() 