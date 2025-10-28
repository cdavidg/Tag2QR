from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Category, db
from app.forms import CategoryForm

category_bp = Blueprint('category', __name__, url_prefix='/admin/category')

@category_bp.route('/')
@login_required
def list_categories():
    """Lista todas las categorías del usuario actual"""
    categories = Category.query.filter_by(
        user_id=current_user.id
    ).order_by(Category.name).all()
    return render_template('admin/category_list.html', categories=categories)

@category_bp.route('/new', methods=['GET', 'POST'])
@login_required
def category_new():
    """Crear nueva categoría"""
    form = CategoryForm()
    
    if form.validate_on_submit():
        # Generar slug
        import re
        slug = re.sub(r'[^\w\s-]', '', form.name.data.lower())
        slug = re.sub(r'[-\s]+', '-', slug).strip('-')
        
        # Verificar que el slug sea único para este usuario
        existing = Category.query.filter_by(
            slug=slug,
            user_id=current_user.id
        ).first()
        if existing:
            user_category_count = Category.query.filter_by(
                user_id=current_user.id
            ).count()
            slug = f"{slug}-{user_category_count + 1}"
        
        category = Category(
            name=form.name.data,
            description=form.description.data,
            slug=slug,
            active=form.active.data,
            user_id=current_user.id
        )
        
        db.session.add(category)
        db.session.commit()
        
        flash('Categoría creada exitosamente', 'success')
        return redirect(url_for('category.list_categories'))
    
    return render_template('admin/category_form.html', form=form, title='Nueva Categoría')

@category_bp.route('/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def category_edit(category_id):
    """Editar categoría"""
    category = Category.query.filter_by(
        id=category_id,
        user_id=current_user.id
    ).first_or_404()
    form = CategoryForm(obj=category)
    
    if form.validate_on_submit():
        category.name = form.name.data
        category.description = form.description.data
        category.active = form.active.data
        
        db.session.commit()
        
        flash('Categoría actualizada exitosamente', 'success')
        return redirect(url_for('category.list_categories'))
    
    return render_template('admin/category_form.html', form=form, category=category, title='Editar Categoría')

@category_bp.route('/<int:category_id>/delete', methods=['POST'])
@login_required
def category_delete(category_id):
    """Eliminar categoría"""
    category = Category.query.filter_by(
        id=category_id,
        user_id=current_user.id
    ).first_or_404()
    
    # Verificar si hay productos asociados
    if category.products.count() > 0:
        flash(f'No se puede eliminar la categoría porque tiene {category.products.count()} producto(s) asociado(s)', 'error')
        return redirect(url_for('category.list_categories'))
    
    db.session.delete(category)
    db.session.commit()
    
    flash('Categoría eliminada exitosamente', 'success')
    return redirect(url_for('category.list_categories'))