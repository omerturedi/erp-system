from flask import Flask, url_for, redirect
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from app.core.config import settings
from app.models.user import User, Role, Module, Company, AuditLog
from app.admin.views import UserView, RoleView, ModuleView, CompanyView, AuditLogView, DashboardView
from app.admin.auth import auth, login_manager

def create_admin():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = settings.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Login manager'ı başlat
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Lütfen giriş yapın.'

    # Auth blueprint'i kaydet
    app.register_blueprint(auth)

    db = SQLAlchemy(app)
    admin = Admin(app, name='ERP Yönetim Sistemi', template_mode='bootstrap4', index_view=DashboardView(url='/admin', endpoint='admin'))

    # Admin görünümlerini ekle
    admin.add_view(UserView(User, db.session, name='Kullanıcılar'))
    admin.add_view(RoleView(Role, db.session, name='Roller'))
    admin.add_view(ModuleView(Module, db.session, name='Modüller'))
    admin.add_view(CompanyView(Company, db.session, name='Şirketler'))
    admin.add_view(AuditLogView(AuditLog, db.session, name='Denetim Günlüğü'))

    # Admin paneline erişim öncesi login kontrolü
    @app.before_request
    def check_admin_login():
        if request.path.startswith('/admin') and not current_user.is_authenticated:
            return redirect(url_for('auth.login'))

    return app 