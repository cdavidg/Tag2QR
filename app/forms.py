from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DecimalField, FileField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, Length, NumberRange, ValidationError, Optional
from wtforms.widgets import TextArea
from flask_wtf.file import FileAllowed
from app.models import User, Product, Category

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    name = StringField('Nombre Completo', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Contraseña', validators=[
        DataRequired(), 
        Length(min=6, message='La contraseña debe tener al menos 6 caracteres')
    ])
    password_confirm = PasswordField('Confirmar Contraseña', validators=[DataRequired()])
    
    def validate_email(self, field):
        # Verificar que el email no esté registrado
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Este email ya está registrado. Por favor, usa otro o inicia sesión.')
    
    def validate_password_confirm(self, field):
        # Verificar que las contraseñas coincidan
        if field.data != self.password.data:
            raise ValidationError('Las contraseñas no coinciden.')

class ProductForm(FlaskForm):
    name = StringField('Nombre del Producto', validators=[DataRequired(), Length(min=1, max=200)])
    sku = StringField('SKU', validators=[DataRequired(), Length(min=1, max=64)])
    category_id = SelectField('Categoría', coerce=int, validators=[Optional()])
    description = TextAreaField('Descripción')
    price = DecimalField('Precio (USD)', validators=[DataRequired(), NumberRange(min=0.01)], places=2)
    active = BooleanField('Activo', default=True)
    images = FileField('Imágenes', 
                      validators=[FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Solo se permiten imágenes!')],
                      render_kw={"multiple": True})
    
    def __init__(self, *args, user_id=None, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        # Cargar categorías dinámicamente filtradas por usuario
        if user_id:
            self.category_id.choices = [(0, '-- Sin categoría --')] + [
                (c.id, c.name) for c in Category.query.filter_by(
                    active=True,
                    user_id=user_id
                ).order_by(Category.name).all()
            ]
        else:
            # Fallback si no se proporciona user_id (no debería pasar)
            self.category_id.choices = [(0, '-- Sin categoría --')]
    
    def validate_sku(self, field):
        # Validar que el SKU sea único para el usuario (excepto si es el mismo producto en edición)
        from flask_login import current_user
        existing_product = Product.query.filter_by(
            sku=field.data,
            created_by=current_user.id
        ).first()
        if existing_product:
            # Si estamos editando, permitir el mismo SKU
            if hasattr(self, 'product_id') and existing_product.id == self.product_id:
                return
            raise ValidationError('Este SKU ya existe en tus productos. Por favor, usa uno diferente.')

class CategoryForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(min=1, max=100)])
    description = TextAreaField('Descripción')
    active = BooleanField('Activa', default=True)

class StoreConfigForm(FlaskForm):
    name = StringField('Nombre de la Tienda', validators=[DataRequired(), Length(min=1, max=200)])
    phone = StringField('Teléfono', validators=[Optional(), Length(max=50)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    address = TextAreaField('Dirección')
    website = StringField('Sitio Web', validators=[Optional(), Length(max=200)])
    logo = FileField('Logo de la Tienda', 
                    validators=[FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Solo se permiten imágenes!')])
    
    # Configuración de etiquetas
    label_show_logo = BooleanField('Mostrar logo en etiqueta', default=True)
    label_show_price = BooleanField('Mostrar precio en etiqueta', default=True)
    label_show_sku = BooleanField('Mostrar SKU en etiqueta', default=True)
    label_show_description = BooleanField('Mostrar descripción en etiqueta', default=False)
    label_font_size = IntegerField('Tamaño de fuente', validators=[NumberRange(min=8, max=24)], default=14)

class LabelTemplateForm(FlaskForm):
    """Formulario para configuración de plantillas de etiquetas"""
    # Tipo de plantilla
    label_template = SelectField('Tipo de Plantilla', 
                                choices=[
                                    ('rectangular', 'Rectangular'),
                                    ('square', 'Cuadrada'),
                                    ('circular', 'Circular')
                                ],
                                default='rectangular')
    
    # Dimensiones
    label_width = IntegerField('Ancho (mm)', 
                              validators=[DataRequired(), NumberRange(min=20, max=200)], 
                              default=80)
    label_height = IntegerField('Alto (mm)', 
                               validators=[DataRequired(), NumberRange(min=20, max=200)], 
                               default=50)
    label_padding = IntegerField('Espaciado interno (mm)', 
                                validators=[DataRequired(), NumberRange(min=0, max=20)], 
                                default=5)
    
    # Tamaño del QR
    label_qr_size = IntegerField('Tamaño del QR (% del ancho)', 
                                validators=[DataRequired(), NumberRange(min=20, max=80)], 
                                default=30)
    
    # Bordes
    label_border = BooleanField('Mostrar borde', default=True)
    label_border_width = IntegerField('Grosor del borde (px)', 
                                     validators=[NumberRange(min=1, max=10)], 
                                     default=1)
    label_border_color = StringField('Color del borde', 
                                    validators=[Length(max=7)], 
                                    default='#000000')
    
    # Colores
    label_background_color = StringField('Color de fondo', 
                                        validators=[Length(max=7)], 
                                        default='#FFFFFF')
    label_text_color = StringField('Color del texto', 
                                  validators=[Length(max=7)], 
                                  default='#000000')
    
    # Contenido
    label_show_store_name = BooleanField('Mostrar nombre de tienda', default=True)
    label_show_product_name = BooleanField('Mostrar nombre de producto', default=True)
    label_show_logo = BooleanField('Mostrar logo', default=True)
    label_show_price = BooleanField('Mostrar precio', default=True)
    label_show_sku = BooleanField('Mostrar SKU', default=True)
    label_show_description = BooleanField('Mostrar descripción', default=False)
    label_font_size = IntegerField('Tamaño de fuente (pt)', 
                                  validators=[NumberRange(min=8, max=24)], 
                                  default=14)

class CreateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Este email ya está registrado.')