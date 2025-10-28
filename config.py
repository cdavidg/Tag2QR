import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///shopqr.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session settings - Mantener login por 30 días
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24 * 30  # 30 días en segundos
    SESSION_COOKIE_SECURE = True  # Solo HTTPS
    SESSION_COOKIE_HTTPONLY = True  # Protección XSS
    SESSION_COOKIE_SAMESITE = 'Lax'  # Protección CSRF
    REMEMBER_COOKIE_DURATION = 60 * 60 * 24 * 30  # 30 días
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
    
    # Upload settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
    
    # Image settings
    MAX_IMAGE_WIDTH = 1024
    THUMBNAIL_WIDTH = 400
    
    # QR settings
    QR_FOLDER = os.path.join(UPLOAD_FOLDER, 'qr')
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}