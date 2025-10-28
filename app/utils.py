import os
import uuid
from werkzeug.utils import secure_filename
from PIL import Image
from flask import current_app
from app.models import ProductImage, db
import random
import string

def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def generate_sku(prefix='PRD'):
    """Genera un SKU único"""
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{prefix}-{random_suffix}"

def create_thumbnail(image_path, thumbnail_path, width=400):
    """Crea un thumbnail de la imagen"""
    try:
        with Image.open(image_path) as img:
            # Convertir a RGB si es necesario (para PNG con transparencia)
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Calcular nueva altura manteniendo proporción
            ratio = width / img.width
            height = int(img.height * ratio)
            
            # Redimensionar
            img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
            img_resized.save(thumbnail_path, 'JPEG', quality=85, optimize=True)
        return True
    except Exception as e:
        print(f"Error creando thumbnail: {e}")
        return False

def resize_image(image_path, max_width=1024):
    """Redimensiona la imagen original si es muy grande"""
    try:
        with Image.open(image_path) as img:
            if img.width > max_width:
                # Convertir a RGB si es necesario
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                ratio = max_width / img.width
                height = int(img.height * ratio)
                
                img_resized = img.resize((max_width, height), Image.Resampling.LANCZOS)
                img_resized.save(image_path, 'JPEG', quality=90, optimize=True)
        return True
    except Exception as e:
        print(f"Error redimensionando imagen: {e}")
        return False

def save_product_images(product_id, files):
    """Guarda múltiples imágenes para un producto"""
    if not files:
        return []
    
    # Crear directorio del producto si no existe
    product_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'products', str(product_id))
    os.makedirs(product_dir, exist_ok=True)
    
    saved_images = []
    
    # Obtener el último orden de imagen para este producto
    last_order = db.session.query(db.func.max(ProductImage.order)).filter_by(product_id=product_id).scalar() or 0
    
    for file in files:
        if file and file.filename and allowed_file(file.filename):
            # Generar nombre único
            original_filename = secure_filename(file.filename)
            name, ext = os.path.splitext(original_filename)
            unique_filename = f"{uuid.uuid4().hex}{ext}"
            
            # Guardar archivo
            file_path = os.path.join(product_dir, unique_filename)
            file.save(file_path)
            
            # Redimensionar imagen original si es necesaria
            resize_image(file_path, current_app.config['MAX_IMAGE_WIDTH'])
            
            # Crear thumbnail
            name_only = os.path.splitext(unique_filename)[0]
            thumbnail_filename = f"{name_only}_thumb.jpg"
            thumbnail_path = os.path.join(product_dir, thumbnail_filename)
            create_thumbnail(file_path, thumbnail_path, current_app.config['THUMBNAIL_WIDTH'])
            
            # Guardar en base de datos
            last_order += 1
            product_image = ProductImage(
                product_id=product_id,
                filename=unique_filename,
                order=last_order
            )
            db.session.add(product_image)
            saved_images.append(product_image)
    
    db.session.commit()
    return saved_images