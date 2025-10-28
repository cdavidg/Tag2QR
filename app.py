import os
from flask import Flask, redirect, url_for, send_from_directory
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from config import config
from app.models import db, User
from app.auth import auth_bp
from app.admin import admin_bp
from app.admin_app import admin_app_bp
from app.public import public_bp
from app.qr_routes import qr_bp
from app.categories import category_bp
from app.store import store_bp

def create_app(config_name=None):
    """Factory para crear la aplicación Flask"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Asegurar que SECRET_KEY esté configurada
    if not app.config.get('SECRET_KEY'):
        app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    
    # Inicializar extensiones
    db.init_app(app)
    migrate = Migrate(app, db)
    csrf = CSRFProtect(app)
    
    # Configurar Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Necesitas iniciar sesión para acceder a esta página.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))
    
    # Registrar filtros personalizados de Jinja2
    @app.template_filter('nl2br')
    def nl2br_filter(text):
        """Convierte saltos de línea en <br> tags"""
        if not text:
            return ''
        from markupsafe import Markup, escape
        text = escape(text)
        text = text.replace('\n', Markup('<br>\n'))
        return text
    
    # Registrar blueprints
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(admin_app_bp)
    app.register_blueprint(qr_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(store_bp)
    
    # Ruta para servir archivos estáticos de uploads
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    # Redirección del admin sin login
    @app.route('/admin')
    def admin_redirect():
        return redirect(url_for('admin.dashboard'))
    
    # Crear tablas y directorios necesarios
    with app.app_context():
        # Crear directorios de uploads si no existen
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'products'), exist_ok=True)
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'store'), exist_ok=True)
        os.makedirs(app.config['QR_FOLDER'], exist_ok=True)
        
        # Crear tablas
        db.create_all()
    
    return app

# Crear la aplicación
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)