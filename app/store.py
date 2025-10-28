from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app.models import Store, db, Product
from app.forms import StoreConfigForm, LabelTemplateForm
from werkzeug.utils import secure_filename
import os
import uuid

store_bp = Blueprint('store', __name__, url_prefix='/admin/store')

@store_bp.route('/config', methods=['GET', 'POST'])
@login_required
def config():
    """Configuración de la tienda"""
    store = Store.get_store(current_user.id)
    form = StoreConfigForm(obj=store)
    
    if form.validate_on_submit():
        store.name = form.name.data
        store.phone = form.phone.data
        store.email = form.email.data
        store.address = form.address.data
        store.website = form.website.data
        
        # Configuración de etiquetas
        store.label_show_logo = form.label_show_logo.data
        store.label_show_price = form.label_show_price.data
        store.label_show_sku = form.label_show_sku.data
        store.label_show_description = form.label_show_description.data
        store.label_font_size = form.label_font_size.data
        
        # Procesar logo si se subió uno nuevo
        if form.logo.data and form.logo.data.filename:
            from PIL import Image
            
            # Crear directorio para el logo
            store_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'store')
            os.makedirs(store_dir, exist_ok=True)
            
            # Eliminar logo anterior si existe
            if store.logo_filename:
                old_logo = os.path.join(store_dir, store.logo_filename)
                if os.path.exists(old_logo):
                    os.remove(old_logo)
            
            # Guardar nuevo logo
            filename = secure_filename(form.logo.data.filename)
            name, ext = os.path.splitext(filename)
            unique_filename = f"logo_{uuid.uuid4().hex}{ext}"
            logo_path = os.path.join(store_dir, unique_filename)
            
            form.logo.data.save(logo_path)
            
            # Redimensionar logo
            try:
                with Image.open(logo_path) as img:
                    if img.mode in ('RGBA', 'LA', 'P'):
                        img = img.convert('RGB')
                    
                    # Redimensionar a máximo 200px de ancho
                    if img.width > 200:
                        ratio = 200 / img.width
                        new_height = int(img.height * ratio)
                        img = img.resize((200, new_height), Image.Resampling.LANCZOS)
                    
                    img.save(logo_path, 'JPEG', quality=90, optimize=True)
            except Exception as e:
                flash(f'Error procesando logo: {str(e)}', 'warning')
            
            store.logo_filename = unique_filename
        
        db.session.commit()
        flash('Configuración actualizada exitosamente', 'success')
        return redirect(url_for('store.config'))
    
    return render_template('admin/store_config.html', form=form, store=store)

@store_bp.route('/label-templates', methods=['GET', 'POST'])
@login_required
def label_templates():
    """Configuración de plantillas de etiquetas"""
    store = Store.get_store(current_user.id)
    form = LabelTemplateForm(obj=store)
    
    # Obtener un producto de ejemplo para la vista previa
    sample_product = Product.query.filter_by(created_by=current_user.id).first()
    
    if form.validate_on_submit():
        # Actualizar configuración de plantilla
        store.label_template = form.label_template.data
        store.label_width = form.label_width.data
        store.label_height = form.label_height.data
        store.label_padding = form.label_padding.data
        store.label_qr_size = form.label_qr_size.data
        store.label_border = form.label_border.data
        store.label_border_width = form.label_border_width.data
        store.label_border_color = form.label_border_color.data
        store.label_background_color = form.label_background_color.data
        store.label_text_color = form.label_text_color.data
        store.label_show_store_name = form.label_show_store_name.data
        store.label_show_product_name = form.label_show_product_name.data
        store.label_show_logo = form.label_show_logo.data
        store.label_show_price = form.label_show_price.data
        store.label_show_sku = form.label_show_sku.data
        store.label_show_description = form.label_show_description.data
        store.label_font_size = form.label_font_size.data
        
        db.session.commit()
        flash('Plantilla de etiqueta actualizada exitosamente', 'success')
        return redirect(url_for('store.label_templates'))
    
    return render_template('admin/label_templates.html', 
                         form=form, 
                         store=store, 
                         sample_product=sample_product)
