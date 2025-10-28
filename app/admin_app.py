"""
Blueprint para el panel de administración de la aplicación (Super Admin)
Accesible desde /admin_app - Solo para superadministradores
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from functools import wraps
from app.models import db, User, Product, Category, Store, ProductView
from sqlalchemy import func, desc
from datetime import datetime, timedelta

admin_app_bp = Blueprint('admin_app', __name__, url_prefix='/admin_app')

def superadmin_required(f):
    """Decorador para requerir permisos de superadministrador"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Debes iniciar sesión para acceder.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        if not current_user.is_superadmin:
            flash('No tienes permisos para acceder a esta sección.', 'danger')
            return redirect(url_for('admin.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@admin_app_bp.before_request
def check_superadmin_access():
    """Verificación global de acceso para todo el blueprint admin_app"""
    if not current_user.is_authenticated:
        flash('Debes iniciar sesión para acceder.', 'warning')
        return redirect(url_for('auth.login', next=request.url))
    if not hasattr(current_user, 'is_superadmin') or not current_user.is_superadmin:
        flash('Acceso denegado. Solo para superadministradores.', 'danger')
        return redirect(url_for('admin.dashboard'))

@admin_app_bp.route('/')
@superadmin_required
def dashboard():
    """Dashboard principal del panel de super administración"""
    
    # Estadísticas generales
    total_users = User.query.count()
    total_products = Product.query.count()
    total_categories = Category.query.count()
    total_stores = Store.query.count()
    
    # Usuarios activos (con productos)
    active_users = db.session.query(User).join(Product).distinct().count()
    
    # Productos creados últimos 30 días
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_products = Product.query.filter(Product.created_at >= thirty_days_ago).count()
    
    # Usuarios registrados últimos 30 días
    recent_users = User.query.filter(User.created_at >= thirty_days_ago).count()
    
    # Productos más visitados (últimos 30 días)
    top_products = db.session.query(
        Product,
        func.count(ProductView.id).label('view_count')
    ).join(
        ProductView, Product.id == ProductView.product_id
    ).filter(
        ProductView.viewed_at >= thirty_days_ago
    ).group_by(
        Product.id
    ).order_by(
        desc('view_count')
    ).limit(10).all()
    
    # Usuarios más activos (por cantidad de productos)
    top_users = db.session.query(
        User,
        func.count(Product.id).label('product_count')
    ).join(
        Product, User.id == Product.created_by
    ).group_by(
        User.id
    ).order_by(
        desc('product_count')
    ).limit(10).all()
    
    # Últimos usuarios registrados
    latest_users = User.query.order_by(User.created_at.desc()).limit(10).all()
    
    # Últimos productos creados
    latest_products = Product.query.order_by(Product.created_at.desc()).limit(10).all()
    
    return render_template('admin_app/dashboard.html',
                         total_users=total_users,
                         total_products=total_products,
                         total_categories=total_categories,
                         total_stores=total_stores,
                         active_users=active_users,
                         recent_products=recent_products,
                         recent_users=recent_users,
                         top_products=top_products,
                         top_users=top_users,
                         latest_users=latest_users,
                         latest_products=latest_products)

@admin_app_bp.route('/users')
@superadmin_required
def user_list():
    """Lista de todos los usuarios del sistema"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    filter_type = request.args.get('filter', 'all', type=str)
    
    # Query base
    query = User.query
    
    # Filtros de búsqueda
    if search:
        query = query.filter(User.email.contains(search))
    
    # Filtros por tipo
    if filter_type == 'superadmin':
        query = query.filter_by(is_superadmin=True)
    elif filter_type == 'admin':
        query = query.filter_by(is_admin=True, is_superadmin=False)
    elif filter_type == 'active':
        # Usuarios con al menos un producto
        query = query.join(Product).distinct()
    elif filter_type == 'inactive':
        # Usuarios sin productos
        query = query.outerjoin(Product).group_by(User.id).having(func.count(Product.id) == 0)
    
    # Paginación
    users = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    # Agregar contadores a cada usuario
    for user in users.items:
        user.product_count = Product.query.filter_by(created_by=user.id).count()
        user.category_count = Category.query.filter_by(user_id=user.id).count()
        user.has_store = Store.query.filter_by(user_id=user.id).first() is not None
    
    return render_template('admin_app/user_list.html',
                         users=users,
                         search=search,
                         filter_type=filter_type)

@admin_app_bp.route('/users/<int:user_id>')
@superadmin_required
def user_detail(user_id):
    """Detalles de un usuario específico"""
    user = User.query.get_or_404(user_id)
    
    # Estadísticas del usuario
    total_products = Product.query.filter_by(created_by=user_id).count()
    total_categories = Category.query.filter_by(user_id=user_id).count()
    store = Store.query.filter_by(user_id=user_id).first()
    
    # Productos del usuario
    products = Product.query.filter_by(created_by=user_id).order_by(
        Product.created_at.desc()
    ).limit(10).all()
    
    # Categorías del usuario
    categories = Category.query.filter_by(user_id=user_id).all()
    
    return render_template('admin_app/user_detail.html',
                         user=user,
                         total_products=total_products,
                         total_categories=total_categories,
                         store=store,
                         products=products,
                         categories=categories)

@admin_app_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@superadmin_required
def user_edit(user_id):
    """Editar usuario - cambiar email, password, permisos"""
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        # Actualizar email
        new_email = request.form.get('email', '').strip()
        if new_email and new_email != user.email:
            # Verificar que el email no esté en uso
            existing = User.query.filter_by(email=new_email).first()
            if existing:
                flash('El email ya está en uso por otro usuario.', 'danger')
            else:
                user.email = new_email
                flash('Email actualizado correctamente.', 'success')
        
        # Actualizar password si se proporciona
        new_password = request.form.get('password', '').strip()
        if new_password:
            user.set_password(new_password)
            flash('Contraseña actualizada correctamente.', 'success')
        
        # Actualizar permisos
        user.is_admin = 'is_admin' in request.form
        
        # Solo permitir cambiar is_superadmin si el usuario actual es superadmin
        # y no se está editando a sí mismo (para evitar quedarse sin acceso)
        if current_user.is_superadmin and user.id != current_user.id:
            user.is_superadmin = 'is_superadmin' in request.form
        
        db.session.commit()
        flash('Usuario actualizado exitosamente.', 'success')
        return redirect(url_for('admin_app.user_detail', user_id=user.id))
    
    return render_template('admin_app/user_edit.html', user=user)

@admin_app_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@superadmin_required
def user_delete(user_id):
    """Eliminar usuario (solo si no tiene productos)"""
    user = User.query.get_or_404(user_id)
    
    # No permitir eliminar al propio usuario
    if user.id == current_user.id:
        flash('No puedes eliminar tu propia cuenta.', 'danger')
        return redirect(url_for('admin_app.user_list'))
    
    # Verificar si tiene productos
    product_count = Product.query.filter_by(created_by=user_id).count()
    if product_count > 0:
        flash(f'No se puede eliminar el usuario porque tiene {product_count} productos asociados.', 'danger')
        return redirect(url_for('admin_app.user_detail', user_id=user.id))
    
    # Eliminar tienda si tiene
    store = Store.query.filter_by(user_id=user_id).first()
    if store:
        db.session.delete(store)
    
    # Eliminar categorías
    Category.query.filter_by(user_id=user_id).delete()
    
    # Eliminar usuario
    email = user.email
    db.session.delete(user)
    db.session.commit()
    
    flash(f'Usuario {email} eliminado exitosamente.', 'success')
    return redirect(url_for('admin_app.user_list'))

@admin_app_bp.route('/users/<int:user_id>/toggle-admin', methods=['POST'])
@superadmin_required
def user_toggle_admin(user_id):
    """Alternar permisos de administrador"""
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('No puedes cambiar tus propios permisos.', 'danger')
        return redirect(url_for('admin_app.user_detail', user_id=user.id))
    
    user.is_admin = not user.is_admin
    db.session.commit()
    
    status = "activados" if user.is_admin else "desactivados"
    flash(f'Permisos de administrador {status} para {user.email}.', 'success')
    
    return redirect(url_for('admin_app.user_detail', user_id=user.id))

@admin_app_bp.route('/products')
@superadmin_required
def product_list():
    """Lista de todos los productos del sistema"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    user_id = request.args.get('user_id', type=int)
    
    # Query base
    query = Product.query
    
    # Filtro por usuario
    if user_id:
        query = query.filter_by(created_by=user_id)
    
    # Filtro por búsqueda
    if search:
        query = query.filter(
            (Product.name.contains(search)) | (Product.sku.contains(search))
        )
    
    # Paginación
    products = query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    # Cargar información de usuarios para cada producto
    for product in products.items:
        product.owner = User.query.get(product.created_by)
    
    # Lista de usuarios para el filtro
    users = User.query.order_by(User.email).all()
    
    return render_template('admin_app/product_list.html',
                         products=products,
                         search=search,
                         selected_user=user_id,
                         users=users)

@admin_app_bp.route('/stores')
@superadmin_required
def store_list():
    """Lista de todas las tiendas configuradas"""
    page = request.args.get('page', 1, type=int)
    
    stores = Store.query.order_by(Store.updated_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    # Agregar contadores a cada tienda
    for store in stores.items:
        store.product_count = Product.query.filter_by(created_by=store.user_id).count()
    
    return render_template('admin_app/store_list.html', stores=stores)

@admin_app_bp.route('/stats')
@superadmin_required
def stats():
    """Estadísticas avanzadas del sistema"""
    
    # Estadísticas por periodo
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Usuarios por periodo
    users_today = User.query.filter(func.date(User.created_at) == today).count()
    users_week = User.query.filter(func.date(User.created_at) >= week_ago).count()
    users_month = User.query.filter(func.date(User.created_at) >= month_ago).count()
    
    # Productos por periodo
    products_today = Product.query.filter(func.date(Product.created_at) == today).count()
    products_week = Product.query.filter(func.date(Product.created_at) >= week_ago).count()
    products_month = Product.query.filter(func.date(Product.created_at) >= month_ago).count()
    
    # Distribución de usuarios por actividad
    users_with_products = db.session.query(User.id).join(Product).distinct().count()
    users_without_products = User.query.count() - users_with_products
    
    return render_template('admin_app/stats.html',
                         users_today=users_today,
                         users_week=users_week,
                         users_month=users_month,
                         products_today=products_today,
                         products_week=products_week,
                         products_month=products_month,
                         users_with_products=users_with_products,
                         users_without_products=users_without_products)
