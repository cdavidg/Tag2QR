from flask import Blueprint, render_template, abort, url_for, request, redirect
from flask_login import current_user
from app.models import Product, ProductView, db

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def index():
    """Página de inicio - redirige al dashboard si el usuario está autenticado"""
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    return render_template('public/index.html')

@public_bp.route('/p/<string:sku>')
def product_view(sku):
    """Vista pública del producto optimizada para móvil"""
    product = Product.query.filter_by(sku=sku, active=True).first()
    if not product:
        abort(404)
    
    # Registrar visita
    view = ProductView(
        product_id=product.id,
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent', '')[:255]
    )
    db.session.add(view)
    db.session.commit()
    
    # URL para compartir
    share_url = url_for('public.product_view', sku=sku, _external=True)
    
    return render_template('public/product.html', 
                         product=product, 
                         share_url=share_url)