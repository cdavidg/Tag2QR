from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from decimal import Decimal
import os

db = SQLAlchemy()

class Store(db.Model):
    """Configuración de la tienda"""
    __tablename__ = 'store'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False, default='MI TIENDA')
    phone = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    address = db.Column(db.Text, nullable=True)
    website = db.Column(db.String(200), nullable=True)
    logo_filename = db.Column(db.String(255), nullable=True)
    
    # Configuración de etiquetas
    label_show_store_name = db.Column(db.Boolean, default=True)
    label_show_product_name = db.Column(db.Boolean, default=True)
    label_show_logo = db.Column(db.Boolean, default=True)
    label_show_price = db.Column(db.Boolean, default=True)
    label_show_sku = db.Column(db.Boolean, default=True)
    label_show_description = db.Column(db.Boolean, default=False)
    label_font_size = db.Column(db.Integer, default=14)
    
    # Configuración de plantillas de impresión
    label_template = db.Column(db.String(20), default='rectangular')  # rectangular, square, circular
    label_width = db.Column(db.Integer, default=80)  # mm
    label_height = db.Column(db.Integer, default=50)  # mm
    label_padding = db.Column(db.Integer, default=5)  # mm
    label_qr_size = db.Column(db.Integer, default=30)  # % del ancho
    label_border = db.Column(db.Boolean, default=True)
    label_border_width = db.Column(db.Integer, default=1)  # px
    label_border_color = db.Column(db.String(7), default='#000000')
    label_background_color = db.Column(db.String(7), default='#FFFFFF')
    label_text_color = db.Column(db.String(7), default='#000000')
    
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación con usuario (uno a uno)
    owner = db.relationship('User', backref=db.backref('user_store', uselist=False, lazy=True))
    
    @staticmethod
    def get_store(user_id):
        """Obtiene o crea la configuración de la tienda para el usuario"""
        store = Store.query.filter_by(user_id=user_id).first()
        if not store:
            store = Store(name='MI TIENDA', user_id=user_id)
            db.session.add(store)
            db.session.commit()
        return store
    
    @property
    def logo_url(self):
        """URL del logo de la tienda"""
        if self.logo_filename:
            from flask import url_for
            return url_for('uploaded_file', filename=f'store/{self.logo_filename}')
        return None

class Category(db.Model):
    """Categorías de productos"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    slug = db.Column(db.String(100), nullable=False, index=True)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    owner = db.relationship('User', backref='categories')
    products = db.relationship('Product', backref='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<Category {self.name}>'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=True, nullable=False)
    is_superadmin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con productos
    products = db.relationship('Product', backref='creator', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(64), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    images = db.relationship('ProductImage', backref='product', 
                           cascade='all, delete-orphan', 
                           order_by='ProductImage.order')
    
    @property
    def main_image(self):
        """Obtiene la imagen principal (primera en orden)"""
        return self.images[0] if self.images else None
    
    @property
    def price_formatted(self):
        """Precio formateado para mostrar"""
        return f"${self.price:.2f}"
    
    def get_public_url(self):
        """URL pública del producto"""
        from flask import url_for
        return url_for('public.product_view', sku=self.sku, _external=True)
    
    def generate_slug(self):
        """Genera slug automáticamente basado en el nombre"""
        import re
        slug = re.sub(r'[^\w\s-]', '', self.name.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')
    
    @property
    def total_views(self):
        """Total de visitas al producto"""
        return self.views.count()
    
    def get_views_by_period(self, days=7):
        """Obtiene visitas de los últimos N días"""
        from datetime import timedelta
        start_date = datetime.utcnow() - timedelta(days=days)
        return self.views.filter(ProductView.viewed_at >= start_date).count()
    
    def record_price_change(self, new_price, user_id=None):
        """Registra un cambio de precio"""
        if self.price != new_price:
            history = PriceHistory(
                product_id=self.id,
                price=new_price,
                changed_by=user_id
            )
            db.session.add(history)
            self.price = new_price
    
    def __repr__(self):
        return f'<Product {self.sku}: {self.name}>'

class ProductImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    order = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def url(self):
        """URL completa de la imagen"""
        from flask import url_for
        return url_for('uploaded_file', filename=f'products/{self.product_id}/{self.filename}')
    
    @property
    def thumbnail_url(self):
        """URL del thumbnail"""
        from flask import url_for
        name, ext = os.path.splitext(self.filename)
        thumb_filename = f"{name}_thumb.jpg"
        return url_for('uploaded_file', filename=f'products/{self.product_id}/{thumb_filename}')
    
    def __repr__(self):
        return f'<ProductImage {self.filename} for Product {self.product_id}>'

class PriceHistory(db.Model):
    """Historial de cambios de precio"""
    __tablename__ = 'price_history'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    changed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    changed_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    # Relaciones
    product = db.relationship('Product', backref=db.backref('price_history', lazy='dynamic', order_by='PriceHistory.changed_at', cascade='all, delete-orphan'))
    user = db.relationship('User')
    
    def __repr__(self):
        return f'<PriceHistory Product {self.product_id}: ${self.price} at {self.changed_at}>'

class ProductView(db.Model):
    """Registro de visitas a productos mediante QR"""
    __tablename__ = 'product_view'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    viewed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)  # IPv6 compatible
    user_agent = db.Column(db.String(255), nullable=True)
    
    # Relaciones
    product = db.relationship('Product', backref=db.backref('views', lazy='dynamic', order_by='ProductView.viewed_at.desc()', cascade='all, delete-orphan'))
    
    def __repr__(self):
        return f'<ProductView Product {self.product_id} at {self.viewed_at}>'