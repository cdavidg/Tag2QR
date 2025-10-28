from flask import Blueprint, send_file, url_for, render_template, current_app
from flask_login import login_required, current_user
from app.models import Product
import qrcode
from io import BytesIO
import os

qr_bp = Blueprint('qr', __name__, url_prefix='/admin')

@qr_bp.route('/product/<int:product_id>/qr')
@login_required
def product_qr_view(product_id):
    """Mostrar página con QR y opciones de impresión"""
    product = Product.query.filter_by(id=product_id, created_by=current_user.id).first_or_404()
    qr_url = url_for('qr.product_qr_image', product_id=product_id)
    print_url = url_for('qr.print_ticket', product_id=product_id)
    
    return render_template('admin/product_qr.html', 
                         product=product, 
                         qr_url=qr_url,
                         print_url=print_url)

@qr_bp.route('/product/<int:product_id>/qr.png')
@login_required
def product_qr_image(product_id):
    """Generar y servir imagen QR"""
    product = Product.query.filter_by(id=product_id, created_by=current_user.id).first_or_404()
    
    # Construir URL pública del producto
    public_url = url_for('public.product_view', sku=product.sku, _external=True)
    
    # Generar QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(public_url)
    qr.make(fit=True)
    
    # Crear imagen
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Guardar en memoria
    img_buffer = BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    return send_file(img_buffer, 
                    mimetype='image/png',
                    as_attachment=False,
                    download_name=f'qr_{product.sku}.png')

@qr_bp.route('/product/<int:product_id>/print-ticket')
@login_required
def print_ticket(product_id):
    """Plantilla imprimible para etiqueta/ticket"""
    from app.models import Store
    
    product = Product.query.filter_by(id=product_id, created_by=current_user.id).first_or_404()
    qr_url = url_for('qr.product_qr_image', product_id=product_id, _external=True)
    
    # Obtener configuración de la tienda del usuario actual
    store = Store.get_store(current_user.id)
    
    # Calcular tamaño exacto del QR en mm basado en el porcentaje y las dimensiones
    label_width = store.label_width or 80
    label_height = store.label_height or 50
    qr_percent = store.label_qr_size or 30
    
    # Para rectangular: QR es un porcentaje del ancho disponible
    # Para cuadrada/circular: QR es un porcentaje del ancho total
    if store.label_template == 'rectangular':
        # En rectangular el QR comparte espacio horizontal, usar % más conservador
        qr_size_mm = (label_width * qr_percent) / 100
    else:
        # En square/circular el QR tiene todo el ancho disponible
        qr_size_mm = (label_width * qr_percent) / 100
    
    return render_template('admin/print_ticket.html', 
                         product=product, 
                         qr_url=qr_url,
                         store=store,
                         qr_size_mm=qr_size_mm)

def save_qr_image(product_id, product_sku):
    """Guardar imagen QR en disco (opcional para cache)"""
    try:
        product_url = url_for('public.product_view', sku=product_sku, _external=True)
        
        # Crear directorio QR si no existe
        qr_dir = current_app.config['QR_FOLDER']
        os.makedirs(qr_dir, exist_ok=True)
        
        # Generar QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(product_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Guardar archivo
        filename = f"qr_{product_sku}_{product_id}.png"
        file_path = os.path.join(qr_dir, filename)
        img.save(file_path)
        
        return filename
    except Exception as e:
        print(f"Error guardando QR: {e}")
        return None