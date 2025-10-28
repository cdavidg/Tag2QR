from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from app.models import Product, ProductImage, Category, PriceHistory, ProductView, db
from app.forms import ProductForm
from app.utils import save_product_images, generate_sku
import os

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
def dashboard():
    """Dashboard principal con lista de productos"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    category_id = request.args.get('category', type=int)
    
    # Filtrar solo productos del usuario actual
    query = Product.query.filter_by(created_by=current_user.id)
    
    # Filtro por búsqueda
    if search:
        query = query.filter(Product.name.contains(search) | Product.sku.contains(search))
    
    # Filtro por categoría específica
    if category_id:
        query = query.filter(Product.category_id == category_id)
    
    products = query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    # Obtener solo las categorías del usuario actual
    categories = Category.query.filter_by(
        user_id=current_user.id, 
        active=True
    ).order_by(Category.name).all()
    
    # Agregar contador de productos a cada categoría
    for category in categories:
        category.product_count = Product.query.filter_by(
            category_id=category.id,
            created_by=current_user.id
        ).count()
    
    # Total de productos del usuario
    total_products = Product.query.filter_by(created_by=current_user.id).count()
    
    # Si no hay filtro de categoría ni búsqueda, agrupar productos por categoría
    products_by_category = None
    if not category_id and not search:
        products_by_category = []
        
        # Productos por cada categoría
        for category in categories:
            category_products = Product.query.filter_by(
                created_by=current_user.id,
                category_id=category.id
            ).order_by(Product.created_at.desc()).all()
            
            if category_products:
                products_by_category.append({
                    'category': category,
                    'products': category_products
                })
        
        # Productos sin categoría
        uncategorized_products = Product.query.filter_by(
            created_by=current_user.id,
            category_id=None
        ).order_by(Product.created_at.desc()).all()
        
        if uncategorized_products:
            products_by_category.append({
                'category': None,
                'products': uncategorized_products
            })
    
    # Estadísticas del dashboard
    from sqlalchemy import func
    from datetime import datetime, timedelta
    
    # Productos más visitados (últimos 30 días) - solo del usuario actual
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    top_products = db.session.query(
        Product,
        func.count(ProductView.id).label('view_count')
    ).join(
        ProductView, Product.id == ProductView.product_id
    ).filter(
        ProductView.viewed_at >= thirty_days_ago,
        Product.created_by == current_user.id
    ).group_by(
        Product.id
    ).order_by(
        func.count(ProductView.id).desc()
    ).limit(10).all()
    
    return render_template('admin/dashboard.html', 
                         products=products, 
                         products_by_category=products_by_category,
                         search=search,
                         categories=categories,
                         selected_category=category_id,
                         top_products=top_products,
                         total_products=total_products)

@admin_bp.route('/product/new', methods=['GET', 'POST'])
@login_required
def product_new():
    """Crear nuevo producto"""
    form = ProductForm(user_id=current_user.id)
    
    if form.validate_on_submit():
        # Generar slug automático si no se proporciona
        slug = form.name.data.lower().replace(' ', '-')
        
        # Crear producto
        product = Product(
            name=form.name.data,
            sku=form.sku.data,
            slug=slug,
            description=form.description.data,
            price=form.price.data,
            active=form.active.data,
            category_id=form.category_id.data if form.category_id.data != 0 else None,
            created_by=current_user.id
        )
        
        db.session.add(product)
        db.session.commit()  # Necesario para obtener el ID
        
        # Registrar precio inicial en el historial
        initial_price = PriceHistory(
            product_id=product.id,
            price=form.price.data,
            changed_by=current_user.id
        )
        db.session.add(initial_price)
        db.session.commit()
        
        # Procesar imágenes si las hay
        if form.images.data:
            try:
                save_product_images(product.id, request.files.getlist('images'))
                flash('Producto creado exitosamente', 'success')
            except Exception as e:
                flash(f'Producto creado pero error al subir imágenes: {str(e)}', 'warning')
        else:
            flash('Producto creado exitosamente', 'success')
        
        return redirect(url_for('admin.product_detail', product_id=product.id))
    
    # Auto-generar SKU sugerido
    if not form.sku.data:
        form.sku.data = generate_sku()
    
    return render_template('admin/product_form.html', form=form, title='Nuevo Producto')

@admin_bp.route('/product/<int:product_id>')
@login_required
def product_detail(product_id):
    """Ver detalles del producto"""
    product = Product.query.filter_by(
        id=product_id, 
        created_by=current_user.id
    ).first_or_404()
    return render_template('admin/product_detail.html', product=product)

@admin_bp.route('/product/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def product_edit(product_id):
    """Editar producto"""
    product = Product.query.filter_by(
        id=product_id,
        created_by=current_user.id
    ).first_or_404()
    form = ProductForm(obj=product, user_id=current_user.id)
    form.product_id = product_id  # Para validación de SKU único
    
    if form.validate_on_submit():
        # Verificar si el precio cambió
        old_price = product.price
        new_price = form.price.data
        
        product.name = form.name.data
        product.sku = form.sku.data
        product.slug = form.name.data.lower().replace(' ', '-')
        product.description = form.description.data
        product.active = form.active.data
        product.category_id = form.category_id.data if form.category_id.data != 0 else None
        
        # Registrar cambio de precio si es diferente
        if old_price != new_price:
            product.price = new_price
            price_change = PriceHistory(
                product_id=product.id,
                price=new_price,
                changed_by=current_user.id
            )
            db.session.add(price_change)
        
        # Procesar nuevas imágenes si las hay
        if form.images.data and any(f.filename for f in request.files.getlist('images')):
            try:
                save_product_images(product.id, request.files.getlist('images'))
            except Exception as e:
                flash(f'Error al subir nuevas imágenes: {str(e)}', 'warning')
        
        db.session.commit()
        flash('Producto actualizado exitosamente', 'success')
        return redirect(url_for('admin.product_detail', product_id=product.id))
    
    return render_template('admin/product_form.html', form=form, product=product, title='Editar Producto')

@admin_bp.route('/product/<int:product_id>/delete', methods=['POST'])
@login_required
def product_delete(product_id):
    """Eliminar producto"""
    product = Product.query.filter_by(
        id=product_id,
        created_by=current_user.id
    ).first_or_404()
    
    # Eliminar archivos de imágenes
    product_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'products', str(product_id))
    if os.path.exists(product_folder):
        import shutil
        shutil.rmtree(product_folder)
    
    db.session.delete(product)
    db.session.commit()
    
    flash('Producto eliminado exitosamente', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/product/<int:product_id>/toggle-active', methods=['POST'])
@login_required
def product_toggle_active(product_id):
    """Activar o desactivar producto"""
    product = Product.query.filter_by(
        id=product_id,
        created_by=current_user.id
    ).first_or_404()
    
    # Cambiar el estado
    product.active = not product.active
    db.session.commit()
    
    # Mensaje flash según el nuevo estado
    if product.active:
        flash(f'Producto "{product.name}" activado exitosamente', 'success')
    else:
        flash(f'Producto "{product.name}" desactivado exitosamente', 'warning')
    
    return redirect(url_for('admin.product_detail', product_id=product_id))

@admin_bp.route('/product-image/<int:image_id>/delete', methods=['POST'])
@login_required
def delete_product_image(image_id):
    """Eliminar imagen específica de un producto"""
    image = ProductImage.query.get_or_404(image_id)
    product_id = image.product_id
    
    # Eliminar archivo físico
    image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'products', str(product_id), image.filename)
    if os.path.exists(image_path):
        os.remove(image_path)
    
    # Eliminar thumbnail si existe
    name, ext = os.path.splitext(image.filename)
    thumb_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'products', str(product_id), f"{name}_thumb{ext}")
    if os.path.exists(thumb_path):
        os.remove(thumb_path)
    
    db.session.delete(image)
    db.session.commit()
    
    return jsonify({'success': True})

@admin_bp.route('/camera-capture')
@login_required
def camera_capture():
    """Interfaz para capturar fotos con la cámara"""
    product_id = request.args.get('product_id', type=int)
    return render_template('admin/camera_capture.html', product_id=product_id)

@admin_bp.route('/camera-capture/save', methods=['POST'])
@login_required
def save_camera_capture():
    """Guardar foto capturada desde la cámara"""
    import base64
    from PIL import Image
    from io import BytesIO
    from datetime import datetime
    
    data = request.get_json()
    image_data = data.get('image')
    product_id = data.get('product_id')
    
    if not image_data or not product_id:
        return jsonify({'success': False, 'error': 'Datos incompletos'}), 400
    
    try:
        # Decodificar imagen base64
        image_data = image_data.split(',')[1]  # Remover "data:image/png;base64,"
        image_bytes = base64.b64decode(image_data)
        
        # Abrir imagen con Pillow
        img = Image.open(BytesIO(image_bytes))
        
        # Convertir a RGB si es necesario
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        
        # Generar nombre de archivo único
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"camera_{timestamp}.jpg"
        
        # Crear directorio del producto si no existe
        product_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'products', str(product_id))
        os.makedirs(product_folder, exist_ok=True)
        
        # Guardar imagen original
        image_path = os.path.join(product_folder, filename)
        img.save(image_path, 'JPEG', quality=85)
        
        # Crear thumbnail
        thumb_name = f"camera_{timestamp}_thumb.jpg"
        thumb_path = os.path.join(product_folder, thumb_name)
        img.thumbnail((300, 300), Image.Resampling.LANCZOS)
        img.save(thumb_path, 'JPEG', quality=85)
        
        # Guardar en base de datos
        product = Product.query.filter_by(
            id=product_id,
            created_by=current_user.id
        ).first_or_404()
        product_image = ProductImage(
            product_id=product_id,
            filename=filename,
            thumbnail=thumb_name
        )
        db.session.add(product_image)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'image_id': product_image.id,
            'url': product_image.url,
            'thumbnail_url': product_image.thumbnail_url
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@admin_bp.route('/barcode-scanner')
@login_required
def barcode_scanner():
    """Interfaz para escanear códigos de barras/QR"""
    return render_template('admin/barcode_scanner.html')

@admin_bp.route('/api/check-product/<sku>')
@login_required
def check_product_by_sku(sku):
    """API para verificar si un producto existe por SKU"""
    # Normalizar SKU recibido
    import re
    from sqlalchemy import func

    sku_clean = (sku or '').strip()

    # Log incoming request for debugging
    current_app.logger.warning(f"[check_product_by_sku] user_id={current_user.id} incoming_sku={repr(sku)} cleaned_sku={repr(sku_clean)}")

    # Primero: búsqueda exacta case-insensitive dentro del usuario
    product = Product.query.filter(
        func.lower(Product.sku) == sku_clean.lower(),
        Product.created_by == current_user.id
    ).first()

    # Si no encontramos, intentar una versión saneada (quitar caracteres no alfanuméricos)
    if not product:
        alt = re.sub(r'[^A-Za-z0-9\-_.]', '', sku_clean)
        current_app.logger.warning(f"[check_product_by_sku] trying alternate sanitized sku={repr(alt)}")
        if alt and alt.lower() != sku_clean.lower():
            product = Product.query.filter(
                func.lower(Product.sku) == alt.lower(),
                Product.created_by == current_user.id
            ).first()

    # Log the outcome
    if product:
        current_app.logger.warning(f"[check_product_by_sku] FOUND product id={product.id} sku={product.sku} user_id={product.created_by}")
    else:
        current_app.logger.warning(f"[check_product_by_sku] NOT FOUND for user_id={current_user.id} sku={repr(sku_clean)}")
    
    if product:
        return jsonify({
            'exists': True,
            'product': {
                'id': product.id,
                'name': product.name,
                'sku': product.sku,
                'price': float(product.price) if product.price is not None else None,
                # 'stock' may not be present on Product in this schema; use getattr as safe fallback
                'stock': getattr(product, 'stock', None),
                'url': url_for('admin.product_detail', product_id=product.id)
            }
        })
    else:
        return jsonify({
            'exists': False,
            'create_url': url_for('admin.product_new')
        })

@admin_bp.route('/product/<int:product_id>/price-chart-data')
@login_required
def price_chart_data(product_id):
    """Obtener datos del historial de precios para la gráfica"""
    product = Product.query.filter_by(
        id=product_id,
        created_by=current_user.id
    ).first_or_404()
    
    # Obtener historial de precios
    price_history = PriceHistory.query.filter_by(
        product_id=product_id
    ).order_by(
        PriceHistory.changed_at
    ).all()
    
    # Formatear datos para la gráfica
    data = []
    for record in price_history:
        data.append({
            'date': record.changed_at.strftime('%Y-%m-%d %H:%M'),
            'timestamp': int(record.changed_at.timestamp() * 1000),
            'price': float(record.price)
        })
    
    return jsonify({
        'success': True,
        'product_name': product.name,
        'data': data
    })

@admin_bp.route('/product/<int:product_id>/views-data')
@login_required
def product_views_data(product_id):
    """Obtener datos de visitas para estadísticas"""
    from datetime import datetime, timedelta
    from sqlalchemy import func
    
    product = Product.query.filter_by(
        id=product_id,
        created_by=current_user.id
    ).first_or_404()
    days = request.args.get('days', 30, type=int)
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Agrupar visitas por día
    views_by_day = db.session.query(
        func.date(ProductView.viewed_at).label('date'),
        func.count(ProductView.id).label('count')
    ).filter(
        ProductView.product_id == product_id,
        ProductView.viewed_at >= start_date
    ).group_by(
        func.date(ProductView.viewed_at)
    ).order_by(
        func.date(ProductView.viewed_at)
    ).all()
    
    # Formatear datos
    data = []
    for view in views_by_day:
        data.append({
            'date': view.date.strftime('%Y-%m-%d') if hasattr(view.date, 'strftime') else str(view.date),
            'count': view.count
        })
    
    return jsonify({
        'success': True,
        'product_name': product.name,
        'total_views': product.total_views,
        'data': data
    })