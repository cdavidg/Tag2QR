# ShopQR

Una aplicación web ligera para gestionar productos con códigos QR, construida con Flask.

## Características

- **Área Pública**: Vista optimizada para móvil de productos via URL/QR
- **Área Admin**: Sistema completo de gestión de productos (CRUD)
- **Códigos QR**: Generación automática que apunta a URLs públicas
- **Imágenes**: Upload múltiple con generación de thumbnails
- **Etiquetas**: Plantillas imprimibles en blanco y negro
- **Responsive**: Diseño mobile-first

## Tecnologías

- **Backend**: Flask (Python 3.11+)
- **Base de datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **ORM**: SQLAlchemy
- **Autenticación**: Flask-Login
- **Formularios**: Flask-WTF
- **QR**: qrcode + Pillow
- **Uploads**: Werkzeug + Pillow para thumbnails

## Instalación

1. **Clonar repositorio**:
```bash
git clone <tu-repo>
cd ShopQR
```

2. **Crear entorno virtual**:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**:
```bash
copy .env.example .env
# Editar .env con tus valores
```

5. **Inicializar base de datos**:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. **Ejecutar aplicación**:
```bash
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

## Primer Uso

1. Al abrir la aplicación por primera vez, serás redirigido a crear un usuario administrador
2. Crea tu cuenta admin
3. Inicia sesión y comienza a agregar productos
4. Cada producto puede tener múltiples imágenes
5. Genera códigos QR e imprime etiquetas desde el área admin

## Estructura de URLs

### Públicas
- `/` - Página de inicio
- `/p/<sku>` - Vista pública del producto (mobile-friendly)

### Admin
- `/admin/login` - Inicio de sesión
- `/admin/` - Dashboard con lista de productos
- `/admin/product/new` - Crear producto
- `/admin/product/<id>/edit` - Editar producto
- `/admin/product/<id>` - Ver detalles
- `/admin/product/<id>/qr` - Ver y descargar QR
- `/admin/product/<id>/print-ticket` - Etiqueta imprimible

## Características Técnicas

### Imágenes
- Formatos soportados: JPG, PNG, WEBP
- Generación automática de thumbnails (400px)
- Redimensionado de originales (max 1024px)
- Upload múltiple por producto

### Códigos QR
- Generación dinámica apuntando a URLs públicas
- Descarga como PNG
- Integración en etiquetas imprimibles

### Diseño
- Tema minimalista blanco y negro
- Mobile-first responsive
- Galería swipeable en móvil
- CSS optimizado para impresión

### Seguridad
- CSRF protection en formularios
- Validación de uploads
- Nombres de archivo seguros
- Autenticación requerida para admin

## Producción

Para producción se recomienda:

1. **Base de datos**: PostgreSQL
2. **Servidor**: Gunicorn + Nginx
3. **HTTPS**: Let's Encrypt
4. **Archivos estáticos**: CDN o S3
5. **Variables de entorno**: Configuración segura

### Ejemplo configuración producción:

```bash
# .env
SECRET_KEY=clave-super-secreta-produccion
DATABASE_URL=postgresql://user:pass@host:5432/shopqr
FLASK_ENV=production
```

## Licencia

MIT License