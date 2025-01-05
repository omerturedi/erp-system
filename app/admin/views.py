from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose
from flask import redirect, url_for, request, flash, render_template
from flask_login import current_user
from wtforms import PasswordField
from werkzeug.security import generate_password_hash
from app.db.session import SessionLocal
from app.models.user import User, Role, Module, Company, AuditLog

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_super_admin()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))

class UserView(SecureModelView):
    column_exclude_list = ['hashed_password']
    column_searchable_list = ['email', 'username']
    column_filters = ['is_active', 'role.name', 'company.name']
    
    form_excluded_columns = ['hashed_password']
    form_extra_fields = {
        'password': PasswordField('Şifre')
    }

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.hashed_password = generate_password_hash(form.password.data)

class RoleView(SecureModelView):
    column_searchable_list = ['name']
    column_filters = ['name']
    can_create = True
    can_edit = True
    can_delete = True

class ModuleView(SecureModelView):
    column_searchable_list = ['name']
    column_filters = ['name', 'is_active']
    can_create = True
    can_edit = True
    can_delete = True

class CompanyView(SecureModelView):
    column_searchable_list = ['name']
    column_filters = ['name', 'is_active']
    can_create = True
    can_edit = True
    can_delete = True

class AuditLogView(SecureModelView):
    can_create = False
    can_edit = False
    can_delete = False
    column_searchable_list = ['action', 'table_name']
    column_filters = ['action', 'table_name', 'created_at']
    column_default_sort = ('created_at', True)  # Tarihe göre sırala (en yeni üstte)

class DashboardView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_super_admin()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))

    @expose('/')
    def index(self):
        db = SessionLocal()
        try:
            # İstatistikler
            user_count = db.query(User).count()
            company_count = db.query(Company).count()
            module_count = db.query(Module).count()
            audit_count = db.query(AuditLog).count()

            # Son aktiviteler
            recent_logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(5).all()

            # Aktif Master Admin'ler
            active_master_admins = (
                db.query(User)
                .join(Role)
                .filter(Role.name == "MASTER_ADMIN", User.is_active == True)
                .limit(5)
                .all()
            )

            return self.render(
                'admin/dashboard.html',
                user_count=user_count,
                company_count=company_count,
                module_count=module_count,
                audit_count=audit_count,
                recent_logs=recent_logs,
                active_master_admins=active_master_admins
            )
        finally:
            db.close() 