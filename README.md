<!-- Multilingual README: English, Arabic, Spanish -->
# 🏷️ Tag2QR — Dynamic QR Product Management System

<div align="center">

![Tag2QR](https://img.shields.io/badge/Tag2QR-v1.0-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![Python](https://img.shields.io/badge/Python-3.8+-yellow)
![License](https://img.shields.io/badge/License-MIT-red)

This repository contains Tag2QR, a Progressive Web App (PWA) that converts physical product tags into dynamic QR codes linked to a live product database.

[🌐 Demo](https://tag2qr.shop) • [📖 Documentation](#documentation) • [🚀 Installation](#installation) • [💡 Features](#features)

</div>

---

## English

### What is Tag2QR?

Tag2QR is a Progressive Web Application (PWA) that enables stores and businesses to create dynamic QR codes for physical product tags. Each QR points to a database entry, so product information (price, description, stock, images) stays up-to-date without reprinting labels.

Key benefits:
- Replace static printed labels with QR links that always show the current data
- Reduce reprinting costs and errors when prices or descriptions change

### Features

- Live updates: Price, stock and descriptions update immediately and are visible after scanning
- Multi-store / multi-user support
- Product management: full CRUD (create/read/update/delete)
- QR generation: single and bulk QR/label export
- Built-in QR & barcode scanner (in-browser via camera)
- Customizable printable label templates (rectangular, square, circular)
- PWA: installable, offline-capable features, service worker
- Role-based access: user, admin (store), superadmin (global control panel)

### Admin Interfaces

- Store Admin (`/admin`): manage products, categories, store settings, generate QR labels, use scanner
- Superadmin Control Panel (`/admin_app`): global user/store/product management, system statistics

### Architecture

```
Tag2QR
├── Frontend: responsive HTML/CSS/JS, PWA
├── Backend: Flask 3.0 + Python 3.12, SQLAlchemy ORM
├── Blueprints: auth, admin (store), admin_app (superadmin), store, category, qr, public
└── Storage: SQLite (dev) or PostgreSQL/MySQL (prod), uploads for images and QR assets
```

### Quick Install (developer)

1. Clone
```
git clone https://github.com/cdavidg/Tag2QR.git
cd Tag2QR
```
2. Virtualenv
```
python3 -m venv venv
source venv/bin/activate
```
3. Install
```
pip install -r requirements.txt
```
4. Configure
```
cp .env.example .env
# edit .env (SECRET_KEY, DATABASE_URL, ...)
```
5. Initialize DB and create admin
```
flask db upgrade    # if using migrations
python create_admin.py
```
6. Run
```
python app.py                 # dev
gunicorn -w 3 -b 127.0.0.1:8000 app:app   # prod
```

### Security notes

- The project protects the superadmin panel with:
  - Template-level conditionals (link visible only for superadmins)
  - Blueprint-level `before_request` checks
  - Route-level `@superadmin_required` decorators
- `is_superadmin` defaults to False for all new users — secure-by-default

---

## العربية (Arabic)

### ما هو Tag2QR؟

Tag2QR هو تطبيق ويب تقدمي (PWA) يتيح لمتاجر الأعمال إنشاء رموز QR ديناميكية على بطاقات المنتجات الفعلية. كل رمز QR يربط إلى سجل في قاعدة بيانات، لذلك تبقى معلومات المنتج (السعر، الوصف، المخزون، الصور) محدثة دون الحاجة لإعادة طباعة الملصقات.

الفوائد الأساسية:
- استبدال الملصقات المطبوعة الثابتة بروابط QR تعرض البيانات الحالية دائمًا
- تقليل تكاليف وإعادة طباعة الملصقات عند تغيير الأسعار أو الأوصاف

### الميزات

- تحديث مباشر: تتغير الأسعار والمخزون والوصف وتصبح متاحة فورًا عند المسح
- دعم متعدد المتاجر والمستخدمين
- إدارة المنتجات: إنشاء، قراءة، تحديث، حذف
- إنشاء رموز QR: فردي وجماعي وتصدير ملصقات
- ماسح QR والباركود مدمج (باستخدام كاميرا المتصفح)
- قوالب ملصقات قابلة للتخصيص للطباعة (مستطيل، مربع، دائري)
- تطبيق ويب تقدمي: قابل للتثبيت، يعمل جزئيًا بدون اتصال، مع Service Worker
- صلاحيات متعددة: مستخدم، مدير متجر، مشرف عام (superadmin)

### واجهات الإدارة

- واجهة مدير المتجر (`/admin`): إدارة المنتجات، التصنيفات، إعدادات المتجر، إنشاء الملصقات، الماسح
- لوحة المشرف العام (`/admin_app`): إدارة المستخدمين والمتاجر والمنتجات على مستوى النظام، إحصاءات عامة

### البنية

```
Tag2QR
├── الواجهة الأمامية: HTML/CSS/JS، PWA
├── الخلفية: Flask 3.0 + Python 3.12، SQLAlchemy
├── Blueprints: auth, admin, admin_app, store, category, qr, public
└── التخزين: SQLite (تطوير) أو PostgreSQL/MySQL (إنتاج)، ملف uploads للصور وملفات QR
```

### التثبيت السريع (للمطور)

1. انسخ المستودع
```
git clone https://github.com/cdavidg/Tag2QR.git
cd Tag2QR
```
2. إنشاء بيئة افتراضية
```
python3 -m venv venv
source venv/bin/activate
```
3. تثبيت المتطلبات
```
pip install -r requirements.txt
```
4. الإعداد
```
cp .env.example .env
# حرر .env (SECRET_KEY, DATABASE_URL, ...)
```
5. تهيئة قاعدة البيانات وإنشاء مشرف
```
flask db upgrade
python create_admin.py
```
6. التشغيل
```
python app.py
gunicorn -w 3 -b 127.0.0.1:8000 app:app
```

### ملاحظات أمنية

- حماية لوحة المشرف العام مطبقة عبر:
  - شروط داخل القوالب لإظهار الرابط فقط للمشرفين
  - فحص عام قبل كل طلب داخل الـ blueprint
  - مزين @superadmin_required على المسارات
- الحقل `is_superadmin` افتراضيًا False لجميع المستخدمين الجدد

---

## Español

Se incluye a continuación la versión original en español con la documentación completa.

(La siguiente sección corresponde al README en español — la versión completa se conserva sin cambios.)

---

<!-- BEGIN SPANISH README -->

# 🏷️ Tag2QR - Sistema de Gestión de Productos con QR Dinámicos

<div align="center">

![Tag2QR](https://img.shields.io/badge/Tag2QR-v1.0-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![Python](https://img.shields.io/badge/Python-3.8+-yellow)
![License](https://img.shields.io/badge/License-MIT-red)

**Convierte etiquetas físicas en códigos QR dinámicos conectados en tiempo real con tu base de datos**

[🌐 Demo](https://tag2qr.shop) • [📖 Documentación](#documentación-adicional) • [🚀 Instalación](#-instalación) • [💡 Características](#-características-principales)

</div>

---

## 📋 Índice

- [¿Qué es Tag2QR?](#-qué-es-tag2qr)
- [Características Principales](#-características-principales)
- [Casos de Uso](#-casos-de-uso)
- [Arquitectura del Sistema](#️-arquitectura-del-sistema)
- [Instalación](#-instalación)
- [Configuración](#️-configuración)
- [Guía de Usuario](#-guía-de-usuario)
- [Tecnologías](#️-tecnologías)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Documentación Adicional](#-documentación-adicional)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)

---

## 🎯 ¿Qué es Tag2QR?

**Tag2QR** es una aplicación web progresiva (PWA) que revoluciona la gestión de productos mediante códigos QR dinámicos. En lugar de imprimir etiquetas con información estática que se vuelve obsoleta, Tag2QR genera códigos QR que enlazan directamente con tu base de datos, mostrando información **siempre actualizada** al escanearlos.

### 💡 El Problema que Resuelve

- ❌ **Etiquetas tradicionales:** Precio impreso → Cambio de precio → Reimprimir etiqueta → Costo y desperdicio
- ✅ **Tag2QR:** Código QR impreso → Cambio de precio en sistema → QR muestra nuevo precio → Sin reimprimir

---

## ✨ Características Principales

### 🛍️ Para Tiendas y Comercios

- **Actualización Instantánea:** Modifica precios, descripciones o stock y los cambios se reflejan inmediatamente al escanear el QR
- **Múltiples Tiendas:** Sistema multiusuario con soporte para múltiples negocios independientes
- **Sin Reimpresión:** Imprime el QR una sola vez y actualiza la información infinitas veces
- **Personalización Total:** Logo, colores, información mostrada en etiquetas y páginas públicas
- **Gestión de Inventario:** Control de stock, categorías, imágenes y descripciones detalladas

### 📱 Experiencia del Cliente

- **Escaneo Rápido:** Cualquier app lectora de QR (cámara del smartphone)
- **Información Completa:** Precio, descripción, disponibilidad, imágenes del producto
- **Sin Apps Necesarias:** Funciona directamente en el navegador
- **Responsive:** Diseño optimizado para móviles, tablets y desktop
- **PWA:** Instalable como app nativa en dispositivos móviles

### 👨‍💼 Panel de Administración

#### Panel de Tienda (`/admin`) - Usuarios Normales
- **Dashboard:** Estadísticas de productos, valor del inventario, productos más vendidos
- **Gestión de Productos:** CRUD completo (crear, leer, actualizar, eliminar)
- **Categorías:** Organización por categorías personalizadas
- **Generación de QR:** 
  - QR individual por producto
  - QR masivos con descarga en lote
  - Etiquetas imprimibles con logo y diseño personalizado
- **Escáner de Códigos:** Lector integrado de QR/barras para búsqueda rápida
- **Configuración de Tienda:** Logo, datos de contacto, plantillas de etiquetas
- **Gestión de Usuarios:** (Solo para administradores de tienda)

#### Panel de Control (`/admin_app`) - Superadministradores
- **Gestión Global de Usuarios:** Crear, editar, eliminar usuarios del sistema
- **Gestión Global de Productos:** Vista completa de productos de todas las tiendas
- **Gestión de Tiendas:** Administrar configuraciones de todas las tiendas
- **Estadísticas Globales:** Métricas del sistema completo
- **Diseño Dark Mode:** Interfaz WordPress-style con tema oscuro profesional
- **Seguridad Multi-Capa:** Autenticación, autorización y validación en cada request

### 🎨 Personalización de Etiquetas

- **Plantillas Disponibles:** Rectangular, cuadrada, circular
- **Elementos Configurables:**
  - Mostrar/ocultar: Logo, nombre tienda, nombre producto, precio, SKU, descripción
  - Tamaño de fuente personalizable
  - Colores: Fondo, texto, borde
  - Dimensiones: Ancho, alto, padding, tamaño QR
  - Estilos de borde

### 🔧 Características Técnicas

- **PWA (Progressive Web App):** Funciona offline, instalable, notificaciones push
- **Multiusuario:** Cada usuario tiene su propia tienda aislada
- **Niveles de Acceso:** Usuario, Administrador, Superadministrador
- **Base de Datos SQLite:** Ligera, sin servidor externo, fácil de respaldar
- **Upload de Imágenes:** Soporte para múltiples imágenes por producto
- **Generación QR on-the-fly:** Los QR se generan dinámicamente según configuración
- **Responsive Design:** CSS moderno con flexbox y grid
- **Font Awesome 6.4.0:** Iconografía profesional
- **Session Management:** Persistencia de sesión con Flask-Login

---

## 💼 Casos de Uso

### 🏪 Tiendas Retail
- Etiquetas de precio en estanterías
- Información de producto sin espacio físico
- Actualizaciones de ofertas/descuentos en tiempo real

### 📦 Almacenes y Logística
- Tracking de productos
- Información de ubicación
- Control de inventario

### 🍽️ Restaurantes y Cafeterías
- Menús digitales actualizables
- Información nutricional y alérgenos
- Precios de temporada

### 🏭 Industria y Manufactura
- Especificaciones técnicas de productos
- Manuales de uso enlazados
- Información de garantía

### 🎨 Galerías y Museos
- Información de obras de arte
- Audio guías enlazadas
- Biografías de artistas

### 🏨 Hoteles y Turismo
- Información de servicios
- Mapas y direcciones
- Precios de excursiones

---

## 🏗️ Arquitectura del Sistema

```
Tag2QR
│
├── Frontend (Responsive HTML5/CSS3/JS)
│   ├── Interfaz Pública (QR Scan Results)
│   ├── Panel de Administración (Store Management)
│   └── Panel de Control (Super Admin)
│
├── Backend (Flask 3.0 + Python 3.12)
│   ├── Blueprints:
│   │   ├── auth_bp (Autenticación)
│   │   ├── admin_bp (Panel de tienda)
│   │   ├── admin_app_bp (Panel de control)
│   │   ├── store_bp (Configuración tienda)
│   │   ├── category_bp (Categorías)
│   │   ├── qr_bp (Generación QR)
│   │   └── public_bp (Páginas públicas)
│   │
│   ├── Models (SQLAlchemy ORM):
│   │   ├── User (Usuarios + Auth)
│   │   ├── Store (Configuración tienda)
│   │   ├── Product (Productos)
│   │   └── Category (Categorías)
│   │
│   └── Security:
│       ├── @login_required
│       ├── @admin_required
│       └── @superadmin_required
│
├── Database (SQLite)
│   └── shopqr.db (Relacional normalizada)
│
└── Storage
    ├── uploads/products/ (Imágenes)
    ├── uploads/qr/ (QR generados)
    └── uploads/store/ (Logos)
```

### 📊 Modelo de Datos

```
User
├── id, email, password_hash
├── name, is_admin, is_superadmin
└── Relaciones: Store (1:1), Products (1:N)

Store
├── id, user_id, name, phone, email
├── logo_filename, address, website
├── label_* (Configuración de etiquetas)
└── Relación: User (N:1)

Product
├── id, user_id, name, sku, barcode
├── description, price, stock, cost
├── category_id, images_json
└── Relaciones: User (N:1), Category (N:1)

Category
├── id, user_id, name, description
└── Relaciones: User (N:1), Products (1:N)
```

---

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes Python)
- Git

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/cdavidg/Tag2QR.git
cd Tag2QR
```

### Paso 2: Crear Entorno Virtual

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\\Scripts\\activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar Variables de Entorno

```bash
cp .env.example .env
```

Edita `.env` con tus configuraciones:

```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=tu-clave-secreta-muy-segura-aqui
DATABASE_URL=sqlite:///instance/shopqr.db
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216  # 16MB
```

### Paso 5: Inicializar Base de Datos

```bash
flask db upgrade  # Si usas migraciones
# O simplemente ejecuta la app (creará la BD automáticamente)
python app.py
```

### Paso 6: Crear Usuario Administrador

```bash
python create_admin.py
```

Sigue las instrucciones para crear tu primer superadministrador.

### Paso 7: Ejecutar la Aplicación

```bash
# Modo desarrollo
python app.py

# Modo producción (con Gunicorn)
gunicorn -w 3 -b 127.0.0.1:8000 app:app
```

La aplicación estará disponible en `http://localhost:5000` (desarrollo) o `http://localhost:8000` (producción).

---

## ⚙️ Configuración

### Variables de Entorno

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `FLASK_APP` | Archivo de entrada | `app.py` |
| `FLASK_ENV` | Entorno de ejecución | `production` |
| `SECRET_KEY` | Clave secreta Flask | *Requerido* |
| `DATABASE_URL` | URL de base de datos | `sqlite:///instance/shopqr.db` |
| `UPLOAD_FOLDER` | Directorio de uploads | `uploads` |
| `MAX_CONTENT_LENGTH` | Tamaño máximo de archivo | `16777216` (16MB) |

### Configuración de Producción

Para entornos de producción, se recomienda:

1. **Servidor WSGI:** Gunicorn, uWSGI
2. **Proxy Inverso:** Nginx, Apache
3. **HTTPS:** Certificado SSL/TLS (Let's Encrypt)
4. **Base de Datos:** Migrar a PostgreSQL o MySQL para alto tráfico
5. **Storage:** AWS S3 o similar para imágenes
6. **Backups:** Automatizar respaldos de DB y uploads

#### Ejemplo con Gunicorn + Nginx

**Gunicorn Service** (`/etc/systemd/system/tag2qr.service`):

```ini
[Unit]
Description=Tag2QR Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/tag2qr
Environment="PATH=/var/www/tag2qr/venv/bin"
ExecStart=/var/www/tag2qr/venv/bin/gunicorn -w 3 -b 127.0.0.1:8000 app:app

[Install]
WantedBy=multi-user.target
```

**Nginx Config** (`/etc/nginx/sites-available/tag2qr`):

```nginx
server {
    listen 80;
    server_name tag2qr.shop www.tag2qr.shop;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/tag2qr/static;
        expires 30d;
    }

    location /uploads {
        alias /var/www/tag2qr/uploads;
        expires 30d;
    }
}
```

---

## 📖 Guía de Usuario

### 🔐 Acceso al Sistema

#### Para Usuarios/Tiendas

1. **Registro:** El superadministrador crea tu cuenta desde `/admin_app`
2. **Login:** Accede en `https://tudominio.com/admin/login`
3. **Primera Configuración:**
   - Ve a "Configuración de Tienda"
   - Sube tu logo
   - Completa datos de contacto
   - Configura plantilla de etiquetas

#### Para Superadministradores

1. **Crear Superadmin:**
   ```bash
   python create_admin.py
   ```
   
2. **Login:** Accede en `https://tudominio.com/admin/login`

3. **Acceso al Panel de Control:**
   - Aparecerá un botón "👑 Panel de Control" en el menú de usuario
   - También puedes acceder directamente a `https://tudominio.com/admin_app`

### 🛒 Gestión de Productos

#### Crear Producto

1. Panel de Administración → "Nuevo Producto"
2. Completa los campos:
   - **Nombre:** Título del producto
   - **SKU:** Código único (opcional, se genera automáticamente)
   - **Código de Barras:** Para escaneo con lector
   - **Categoría:** Selecciona o crea nueva
   - **Precio:** Precio de venta
   - **Costo:** Costo de adquisición (opcional)
   - **Stock:** Cantidad disponible
   - **Descripción:** Texto detallado (soporta markdown)
   - **Imágenes:** Hasta 5 imágenes
3. Guardar

#### Generar QR

**QR Individual:**
1. Ve al detalle del producto
2. Clic en "Generar QR"
3. Descarga la imagen PNG

**QR Masivo:**
1. Panel → "Etiquetas"
2. Selecciona productos (checkbox)
3. "Generar Etiquetas Seleccionadas"
4. Descarga PDF con todas las etiquetas

**Configurar Diseño:**
1. Panel → "Configuración de Tienda" → "Plantillas de Etiquetas"
2. Ajusta:
   - Tipo de plantilla (rectangular/cuadrada/circular)
   - Elementos visibles
   - Colores y fuentes
   - Tamaño de etiqueta
3. Vista previa en tiempo real
4. Guardar configuración

### 🔍 Escáner de Productos

El escáner integrado permite buscar productos rápidamente:

1. Panel → "Escáner" (icono de cámara)
2. Permite acceso a la cámara
3. Enfoca el código de barras o QR
4. Resultado automático:
   - ✅ Producto encontrado → Muestra detalles y stock
   - ❌ No encontrado → Opción de crear nuevo producto

**Funciones del Escáner:**
- Búsqueda por código de barras EAN/UPC
- Búsqueda por SKU de productos propios
- Autoenfoque y detección automática
- Funciona con códigos QR y barras

### 👥 Gestión de Usuarios (Superadmin)

**Crear Usuario:**
1. Panel de Control → "Usuarios" → "Nuevo Usuario"
2. Completa datos:
   - Email (login único)
   - Nombre completo
   - Contraseña
   - Permisos: Usuario / Administrador / Superadministrador
3. Guardar

**Editar Usuario:**
1. Lista de usuarios → "Editar"
2. Modifica datos (excepto email)
3. Puedes cambiar contraseña
4. Ajustar permisos

**Eliminar Usuario:**
1. Lista de usuarios → "Eliminar"
2. Confirmar acción
3. ⚠️ Los productos del usuario NO se eliminan

### 📊 Estadísticas y Reportes

**Dashboard de Tienda:**
- Total de productos
- Valor del inventario (costo y venta)
- Productos con bajo stock
- Productos más vendidos (si integras ventas)

**Dashboard de Superadmin:**
- Total de usuarios registrados
- Total de tiendas activas
- Total de productos en sistema
- Productos creados últimos 30 días
- Gráficas de crecimiento

---

## 🛠️ Tecnologías

### Backend

- **Flask 3.0.0:** Framework web Python
- **Flask-SQLAlchemy 3.1.1:** ORM para base de datos
- **Flask-Login 0.6.3:** Gestión de sesiones
- **Flask-WTF 1.2.1:** Formularios y CSRF protection
- **Flask-Migrate 4.0.5:** Migraciones de base de datos
- **Werkzeug 3.0.1:** Utilidades WSGI
- **qrcode[pil] 7.4.2:** Generación de códigos QR
- **Pillow 10.0+:** Procesamiento de imágenes

### Frontend

- **HTML5:** Estructura semántica
- **CSS3:** Diseño moderno (Flexbox, Grid, Variables CSS)
- **JavaScript Vanilla:** Sin dependencias pesadas
- **Font Awesome 6.4.0:** Iconografía
- **html5-qrcode:** Escáner de QR/barras en navegador
- **Service Worker:** PWA functionality

### Base de Datos

- **SQLite:** Desarrollo y pequeñas instalaciones
- **PostgreSQL/MySQL:** Recomendado para producción a gran escala

### Herramientas de Desarrollo

- **Python-dotenv:** Gestión de variables de entorno
- **Gunicorn:** Servidor WSGI para producción
- **Git:** Control de versiones

---

## 📁 Estructura del Proyecto

```
Tag2QR/
│
├── app/                          # Módulos de la aplicación
│   ├── __init__.py              # Factory pattern + blueprints
│   ├── models.py                # Modelos SQLAlchemy
│   ├── forms.py                 # Formularios WTForms
│   ├── auth.py                  # Blueprint: Autenticación
│   ├── admin.py                 # Blueprint: Panel de tienda
│   ├── admin_app.py             # Blueprint: Panel de control
│   ├── store.py                 # Blueprint: Config tienda
│   ├── categories.py            # Blueprint: Categorías
│   ├── qr_routes.py             # Blueprint: Generación QR
│   ├── public.py                # Blueprint: Páginas públicas
│   └── utils.py                 # Utilidades y helpers
│
├── templates/                    # Plantillas Jinja2
│   ├── base.html                # Template base
│   ├── admin/                   # Templates del panel tienda
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── product_form.html
│   │   ├── product_detail.html
│   │   ├── barcode_scanner.html
│   │   ├── store_config.html
│   │   └── ...
│   ├── admin_app/               # Templates del panel control
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── user_list.html
│   │   └── ...
│   └── public/                  # Templates públicos
│       ├── index.html
│       └── product.html
│
├── static/                       # Archivos estáticos
│   ├── css/
│   │   └── style.css            # Estilos globales
│   ├── js/
│   │   └── main.js              # JavaScript global
│   ├── icons/                   # Iconos PWA
│   ├── manifest.json            # PWA manifest
│   └── service-worker.js        # Service Worker PWA
│
├── uploads/                      # Archivos subidos (no en Git)
│   ├── products/                # Imágenes de productos
│   ├── qr/                      # QR generados
│   └── store/                   # Logos de tiendas
│
├── instance/                     # Instancia de la app (no en Git)
│   └── shopqr.db               # Base de datos SQLite
│
├── app.py                       # Punto de entrada
├── config.py                    # Configuración de la app
├── requirements.txt             # Dependencias Python
├── .env.example                 # Template de variables de entorno
├── .gitignore                   # Archivos ignorados por Git
├── create_admin.py              # Script: Crear superadmin
├── manage_users.py              # Script: Gestión de usuarios CLI
│
├── README.md                    # Este archivo
├── MULTIUSUARIO_README.md       # Guía multiusuario
├── PWA_README.md                # Guía PWA
├── ADMIN_APP_STYLE_GUIDE.md     # Guía de diseño panel control
└── SECURITY_ADMIN_APP.md        # Documentación de seguridad
```

---

## 📚 Documentación Adicional

- **[MULTIUSUARIO_README.md](MULTIUSUARIO_README.md):** Guía detallada del sistema multiusuario
- **[PWA_README.md](PWA_README.md):** Configuración y uso como Progressive Web App
- **[ADMIN_APP_STYLE_GUIDE.md](ADMIN_APP_STYLE_GUIDE.md):** Guía de diseño del panel de control
- **[SECURITY_ADMIN_APP.md](SECURITY_ADMIN_APP.md):** Medidas de seguridad implementadas

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Este es un proyecto de código abierto diseñado para la comunidad.

### Cómo Contribuir

1. **Fork** el repositorio
2. **Crea** una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add: Amazing Feature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. **Abre** un Pull Request

### Guías de Estilo

- **Python:** Sigue PEP 8
- **JavaScript:** Usa ESLint con Airbnb style guide
- **CSS:** BEM methodology para clases
- **Commits:** Conventional Commits (feat:, fix:, docs:, style:, refactor:, test:, chore:)

### Reportar Bugs

Abre un [issue](https://github.com/cdavidg/Tag2QR/issues) con:
- Descripción clara del bug
- Pasos para reproducir
- Comportamiento esperado vs actual
- Screenshots si aplica
- Entorno (OS, Python version, navegador)

### Solicitar Features

Abre un [issue](https://github.com/cdavidg/Tag2QR/issues) con:
- Descripción detallada del feature
- Casos de uso
- Mockups o ejemplos (opcional)

---

## 🔮 Roadmap

### v1.1 (Próxima versión)
- [ ] Integración con APIs de e-commerce (WooCommerce, Shopify)
- [ ] Exportación de inventario (CSV, Excel)
- [ ] Modo multidioma (i18n)
- [ ] Notificaciones push por bajo stock
- [ ] Historial de cambios de precio

### v2.0 (Futuro)
- [ ] Dashboard de ventas integrado
- [ ] Generación de reportes PDF
- [ ] API REST para integraciones
- [ ] Soporte para PostgreSQL
- [ ] Sistema de roles personalizable
- [ ] Multi-sucursal por tienda
- [ ] Integración con impresoras térmicas
- [ ] App móvil nativa (React Native)

---

## 📄 Licencia

Este proyecto está licenciado bajo la **Licencia MIT** - ver el archivo [LICENSE](LICENSE) para más detalles.

```
MIT License

Copyright (c) 2025 David García

Se concede permiso, de forma gratuita, a cualquier persona que obtenga una copia
de este software y de los archivos de documentación asociados (el "Software"), 
para utilizar el Software sin restricción, incluyendo sin limitación los derechos 
a usar, copiar, modificar, fusionar, publicar, distribuir, sublicenciar, y/o vender 
copias del Software.
```

---

## 👨‍💻 Autor

**David García**
- GitHub: [@cdavidg](https://github.com/cdavidg)
- Email: cedav95@gmail.com
- Website: [tag2qr.shop](https://tag2qr.shop)

---

## 🙏 Agradecimientos

- A la comunidad de Flask por un framework increíble
- A todos los contribuidores de las librerías open source utilizadas
- A la comunidad de desarrolladores que hacen posible el software libre

---

## 📞 Soporte

¿Tienes preguntas? ¿Necesitas ayuda?

- 📧 Email: cedav95@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/cdavidg/Tag2QR/issues)
- 💬 Discusiones: [GitHub Discussions](https://github.com/cdavidg/Tag2QR/discussions)

---

<div align="center">

**⭐ Si este proyecto te resulta útil, considera darle una estrella en GitHub ⭐**

Made with ❤️ for the Open Source Community

</div>
# 🏷️ Tag2QR - Sistema de Gestión de Productos con QR Dinámicos

<div align="center">

![Tag2QR](https://img.shields.io/badge/Tag2QR-v1.0-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![Python](https://img.shields.io/badge/Python-3.8+-yellow)
![License](https://img.shields.io/badge/License-MIT-red)

**Convierte etiquetas físicas en códigos QR dinámicos conectados en tiempo real con tu base de datos**

[🌐 Demo](https://tag2qr.shop) • [📖 Documentación](#documentación-adicional) • [🚀 Instalación](#instalación) • [💡 Características](#características-principales)

</div>

---

## 📋 Índice

- [¿Qué es Tag2QR?](#-qué-es-tag2qr)
- [Características Principales](#-características-principales)
- [Casos de Uso](#-casos-de-uso)
- [Arquitectura del Sistema](#️-arquitectura-del-sistema)
- [Instalación](#-instalación)
- [Configuración](#️-configuración)
- [Guía de Usuario](#-guía-de-usuario)
- [Tecnologías](#️-tecnologías)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Documentación Adicional](#-documentación-adicional)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)

---

## 🎯 ¿Qué es Tag2QR?

**Tag2QR** es una aplicación web progresiva (PWA) que revoluciona la gestión de productos mediante códigos QR dinámicos. En lugar de imprimir etiquetas con información estática que se vuelve obsoleta, Tag2QR genera códigos QR que enlazan directamente con tu base de datos, mostrando información **siempre actualizada** al escanearlos.

### 💡 El Problema que Resuelve

- ❌ **Etiquetas tradicionales:** Precio impreso → Cambio de precio → Reimprimir etiqueta → Costo y desperdicio
- ✅ **Tag2QR:** Código QR impreso → Cambio de precio en sistema → QR muestra nuevo precio → Sin reimprimir

---

## ✨ Características Principales

### 🛍️ Para Tiendas y Comercios

- **Actualización Instantánea:** Modifica precios, descripciones o stock y los cambios se reflejan inmediatamente al escanear el QR
- **Múltiples Tiendas:** Sistema multiusuario con soporte para múltiples negocios independientes
- **Sin Reimpresión:** Imprime el QR una sola vez y actualiza la información infinitas veces
- **Personalización Total:** Logo, colores, información mostrada en etiquetas y páginas públicas
- **Gestión de Inventario:** Control de stock, categorías, imágenes y descripciones detalladas

### 📱 Experiencia del Cliente

- **Escaneo Rápido:** Cualquier app lectora de QR (cámara del smartphone)
- **Información Completa:** Precio, descripción, disponibilidad, imágenes del producto
- **Sin Apps Necesarias:** Funciona directamente en el navegador
- **Responsive:** Diseño optimizado para móviles, tablets y desktop
- **PWA:** Instalable como app nativa en dispositivos móviles

### 👨‍💼 Panel de Administración

#### Panel de Tienda (`/admin`) - Usuarios Normales
- **Dashboard:** Estadísticas de productos, valor del inventario, productos más vendidos
- **Gestión de Productos:** CRUD completo (crear, leer, actualizar, eliminar)
- **Categorías:** Organización por categorías personalizadas
- **Generación de QR:** 
  - QR individual por producto
  - QR masivos con descarga en lote
  - Etiquetas imprimibles con logo y diseño personalizado
- **Escáner de Códigos:** Lector integrado de QR/barras para búsqueda rápida
- **Configuración de Tienda:** Logo, datos de contacto, plantillas de etiquetas
- **Gestión de Usuarios:** (Solo para administradores de tienda)

#### Panel de Control (`/admin_app`) - Superadministradores
- **Gestión Global de Usuarios:** Crear, editar, eliminar usuarios del sistema
- **Gestión Global de Productos:** Vista completa de productos de todas las tiendas
- **Gestión de Tiendas:** Administrar configuraciones de todas las tiendas
- **Estadísticas Globales:** Métricas del sistema completo
- **Diseño Dark Mode:** Interfaz WordPress-style con tema oscuro profesional
- **Seguridad Multi-Capa:** Autenticación, autorización y validación en cada request

### 🎨 Personalización de Etiquetas

- **Plantillas Disponibles:** Rectangular, cuadrada, circular
- **Elementos Configurables:**
  - Mostrar/ocultar: Logo, nombre tienda, nombre producto, precio, SKU, descripción
  - Tamaño de fuente personalizable
  - Colores: Fondo, texto, borde
  - Dimensiones: Ancho, alto, padding, tamaño QR
  - Estilos de borde

### 🔧 Características Técnicas

- **PWA (Progressive Web App):** Funciona offline, instalable, notificaciones push
- **Multiusuario:** Cada usuario tiene su propia tienda aislada
- **Niveles de Acceso:** Usuario, Administrador, Superadministrador
- **Base de Datos SQLite:** Ligera, sin servidor externo, fácil de respaldar
- **Upload de Imágenes:** Soporte para múltiples imágenes por producto
- **Generación QR on-the-fly:** Los QR se generan dinámicamente según configuración
- **Responsive Design:** CSS moderno con flexbox y grid
- **Font Awesome 6.4.0:** Iconografía profesional
- **Session Management:** Persistencia de sesión con Flask-Login

---

## 💼 Casos de Uso

### 🏪 Tiendas Retail
- Etiquetas de precio en estanterías
- Información de producto sin espacio físico
- Actualizaciones de ofertas/descuentos en tiempo real

### 📦 Almacenes y Logística
- Tracking de productos
- Información de ubicación
- Control de inventario

### 🍽️ Restaurantes y Cafeterías
- Menús digitales actualizables
- Información nutricional y alérgenos
- Precios de temporada

### 🏭 Industria y Manufactura
- Especificaciones técnicas de productos
- Manuales de uso enlazados
- Información de garantía

### 🎨 Galerías y Museos
- Información de obras de arte
- Audio guías enlazadas
- Biografías de artistas

### 🏨 Hoteles y Turismo
- Información de servicios
- Mapas y direcciones
- Precios de excursiones

---

## 🏗️ Arquitectura del Sistema

```
Tag2QR
│
├── Frontend (Responsive HTML5/CSS3/JS)
│   ├── Interfaz Pública (QR Scan Results)
│   ├── Panel de Administración (Store Management)
│   └── Panel de Control (Super Admin)
│
├── Backend (Flask 3.0 + Python 3.12)
│   ├── Blueprints:
│   │   ├── auth_bp (Autenticación)
│   │   ├── admin_bp (Panel de tienda)
│   │   ├── admin_app_bp (Panel de control)
│   │   ├── store_bp (Configuración tienda)
│   │   ├── category_bp (Categorías)
│   │   ├── qr_bp (Generación QR)
│   │   └── public_bp (Páginas públicas)
│   │
│   ├── Models (SQLAlchemy ORM):
│   │   ├── User (Usuarios + Auth)
│   │   ├── Store (Configuración tienda)
│   │   ├── Product (Productos)
│   │   └── Category (Categorías)
│   │
│   └── Security:
│       ├── @login_required
│       ├── @admin_required
│       └── @superadmin_required
│
├── Database (SQLite)
│   └── shopqr.db (Relacional normalizada)
│
└── Storage
    ├── uploads/products/ (Imágenes)
    ├── uploads/qr/ (QR generados)
    └── uploads/store/ (Logos)
```

### 📊 Modelo de Datos

```
User
├── id, email, password_hash
├── name, is_admin, is_superadmin
└── Relaciones: Store (1:1), Products (1:N)

Store
├── id, user_id, name, phone, email
├── logo_filename, address, website
├── label_* (Configuración de etiquetas)
└── Relación: User (N:1)

Product
├── id, user_id, name, sku, barcode
├── description, price, stock, cost
├── category_id, images_json
└── Relaciones: User (N:1), Category (N:1)

Category
├── id, user_id, name, description
└── Relaciones: User (N:1), Products (1:N)
```

---

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes Python)
- Git

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/cdavidg/Tag2QR.git
cd Tag2QR
```

### Paso 2: Crear Entorno Virtual

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar Variables de Entorno

```bash
cp .env.example .env
```

Edita `.env` con tus configuraciones:

```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=tu-clave-secreta-muy-segura-aqui
DATABASE_URL=sqlite:///instance/shopqr.db
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216  # 16MB
```

### Paso 5: Inicializar Base de Datos

```bash
flask db upgrade  # Si usas migraciones
# O simplemente ejecuta la app (creará la BD automáticamente)
python app.py
```

### Paso 6: Crear Usuario Administrador

```bash
python create_admin.py
```

Sigue las instrucciones para crear tu primer superadministrador.

### Paso 7: Ejecutar la Aplicación

```bash
# Modo desarrollo
python app.py

# Modo producción (con Gunicorn)
gunicorn -w 3 -b 127.0.0.1:8000 app:app
```

La aplicación estará disponible en `http://localhost:5000` (desarrollo) o `http://localhost:8000` (producción).

---

## ⚙️ Configuración

### Variables de Entorno

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `FLASK_APP` | Archivo de entrada | `app.py` |
| `FLASK_ENV` | Entorno de ejecución | `production` |
| `SECRET_KEY` | Clave secreta Flask | *Requerido* |
| `DATABASE_URL` | URL de base de datos | `sqlite:///instance/shopqr.db` |
| `UPLOAD_FOLDER` | Directorio de uploads | `uploads` |
| `MAX_CONTENT_LENGTH` | Tamaño máximo de archivo | `16777216` (16MB) |

### Configuración de Producción

Para entornos de producción, se recomienda:

1. **Servidor WSGI:** Gunicorn, uWSGI
2. **Proxy Inverso:** Nginx, Apache
3. **HTTPS:** Certificado SSL/TLS (Let's Encrypt)
4. **Base de Datos:** Migrar a PostgreSQL o MySQL para alto tráfico
5. **Storage:** AWS S3 o similar para imágenes
6. **Backups:** Automatizar respaldos de DB y uploads

#### Ejemplo con Gunicorn + Nginx

**Gunicorn Service** (`/etc/systemd/system/tag2qr.service`):

```ini
[Unit]
Description=Tag2QR Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/tag2qr
Environment="PATH=/var/www/tag2qr/venv/bin"
ExecStart=/var/www/tag2qr/venv/bin/gunicorn -w 3 -b 127.0.0.1:8000 app:app

[Install]
WantedBy=multi-user.target
```

**Nginx Config** (`/etc/nginx/sites-available/tag2qr`):

```nginx
server {
    listen 80;
    server_name tag2qr.shop www.tag2qr.shop;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/tag2qr/static;
        expires 30d;
    }

    location /uploads {
        alias /var/www/tag2qr/uploads;
        expires 30d;
    }
}
```

---

## 📖 Guía de Usuario

### 🔐 Acceso al Sistema

#### Para Usuarios/Tiendas

1. **Registro:** El superadministrador crea tu cuenta desde `/admin_app`
2. **Login:** Accede en `https://tudominio.com/admin/login`
3. **Primera Configuración:**
   - Ve a "Configuración de Tienda"
   - Sube tu logo
   - Completa datos de contacto
   - Configura plantilla de etiquetas

#### Para Superadministradores

1. **Crear Superadmin:**
   ```bash
   python create_admin.py
   ```
   
2. **Login:** Accede en `https://tudominio.com/admin/login`

3. **Acceso al Panel de Control:**
   - Aparecerá un botón "👑 Panel de Control" en el menú de usuario
   - También puedes acceder directamente a `https://tudominio.com/admin_app`

### 🛒 Gestión de Productos

#### Crear Producto

1. Panel de Administración → "Nuevo Producto"
2. Completa los campos:
   - **Nombre:** Título del producto
   - **SKU:** Código único (opcional, se genera automáticamente)
   - **Código de Barras:** Para escaneo con lector
   - **Categoría:** Selecciona o crea nueva
   - **Precio:** Precio de venta
   - **Costo:** Costo de adquisición (opcional)
   - **Stock:** Cantidad disponible
   - **Descripción:** Texto detallado (soporta markdown)
   - **Imágenes:** Hasta 5 imágenes
3. Guardar

#### Generar QR

**QR Individual:**
1. Ve al detalle del producto
2. Clic en "Generar QR"
3. Descarga la imagen PNG

**QR Masivo:**
1. Panel → "Etiquetas"
2. Selecciona productos (checkbox)
3. "Generar Etiquetas Seleccionadas"
4. Descarga PDF con todas las etiquetas

**Configurar Diseño:**
1. Panel → "Configuración de Tienda" → "Plantillas de Etiquetas"
2. Ajusta:
   - Tipo de plantilla (rectangular/cuadrada/circular)
   - Elementos visibles
   - Colores y fuentes
   - Tamaño de etiqueta
3. Vista previa en tiempo real
4. Guardar configuración

### 🔍 Escáner de Productos

El escáner integrado permite buscar productos rápidamente:

1. Panel → "Escáner" (icono de cámara)
2. Permite acceso a la cámara
3. Enfoca el código de barras o QR
4. Resultado automático:
   - ✅ Producto encontrado → Muestra detalles y stock
   - ❌ No encontrado → Opción de crear nuevo producto

**Funciones del Escáner:**
- Búsqueda por código de barras EAN/UPC
- Búsqueda por SKU de productos propios
- Autoenfoque y detección automática
- Funciona con códigos QR y barras

### 👥 Gestión de Usuarios (Superadmin)

**Crear Usuario:**
1. Panel de Control → "Usuarios" → "Nuevo Usuario"
2. Completa datos:
   - Email (login único)
   - Nombre completo
   - Contraseña
   - Permisos: Usuario / Administrador / Superadministrador
3. Guardar

**Editar Usuario:**
1. Lista de usuarios → "Editar"
2. Modifica datos (excepto email)
3. Puedes cambiar contraseña
4. Ajustar permisos

**Eliminar Usuario:**
1. Lista de usuarios → "Eliminar"
2. Confirmar acción
3. ⚠️ Los productos del usuario NO se eliminan

### 📊 Estadísticas y Reportes

**Dashboard de Tienda:**
- Total de productos
- Valor del inventario (costo y venta)
- Productos con bajo stock
- Productos más vendidos (si integras ventas)

**Dashboard de Superadmin:**
- Total de usuarios registrados
- Total de tiendas activas
- Total de productos en sistema
- Productos creados últimos 30 días
- Gráficas de crecimiento

---

## 🛠️ Tecnologías

### Backend

- **Flask 3.0.0:** Framework web Python
- **Flask-SQLAlchemy 3.1.1:** ORM para base de datos
- **Flask-Login 0.6.3:** Gestión de sesiones
- **Flask-WTF 1.2.1:** Formularios y CSRF protection
- **Flask-Migrate 4.0.5:** Migraciones de base de datos
- **Werkzeug 3.0.1:** Utilidades WSGI
- **qrcode[pil] 7.4.2:** Generación de códigos QR
- **Pillow 10.0+:** Procesamiento de imágenes

### Frontend

- **HTML5:** Estructura semántica
- **CSS3:** Diseño moderno (Flexbox, Grid, Variables CSS)
- **JavaScript Vanilla:** Sin dependencias pesadas
- **Font Awesome 6.4.0:** Iconografía
- **html5-qrcode:** Escáner de QR/barras en navegador
- **Service Worker:** PWA functionality

### Base de Datos

- **SQLite:** Desarrollo y pequeñas instalaciones
- **PostgreSQL/MySQL:** Recomendado para producción a gran escala

### Herramientas de Desarrollo

- **Python-dotenv:** Gestión de variables de entorno
- **Gunicorn:** Servidor WSGI para producción
- **Git:** Control de versiones

---

## 📁 Estructura del Proyecto

```
Tag2QR/
│
├── app/                          # Módulos de la aplicación
│   ├── __init__.py              # Factory pattern + blueprints
│   ├── models.py                # Modelos SQLAlchemy
│   ├── forms.py                 # Formularios WTForms
│   ├── auth.py                  # Blueprint: Autenticación
│   ├── admin.py                 # Blueprint: Panel de tienda
│   ├── admin_app.py             # Blueprint: Panel de control
│   ├── store.py                 # Blueprint: Config tienda
│   ├── categories.py            # Blueprint: Categorías
│   ├── qr_routes.py             # Blueprint: Generación QR
│   ├── public.py                # Blueprint: Páginas públicas
│   └── utils.py                 # Utilidades y helpers
│
├── templates/                    # Plantillas Jinja2
│   ├── base.html                # Template base
│   ├── admin/                   # Templates del panel tienda
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── product_form.html
│   │   ├── product_detail.html
│   │   ├── barcode_scanner.html
│   │   ├── store_config.html
│   │   └── ...
│   ├── admin_app/               # Templates del panel control
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── user_list.html
│   │   └── ...
│   └── public/                  # Templates públicos
│       ├── index.html
│       └── product.html
│
├── static/                       # Archivos estáticos
│   ├── css/
│   │   └── style.css            # Estilos globales
│   ├── js/
│   │   └── main.js              # JavaScript global
│   ├── icons/                   # Iconos PWA
│   ├── manifest.json            # PWA manifest
│   └── service-worker.js        # Service Worker PWA
│
├── uploads/                      # Archivos subidos (no en Git)
│   ├── products/                # Imágenes de productos
│   ├── qr/                      # QR generados
│   └── store/                   # Logos de tiendas
│
├── instance/                     # Instancia de la app (no en Git)
│   └── shopqr.db               # Base de datos SQLite
│
├── app.py                       # Punto de entrada
├── config.py                    # Configuración de la app
├── requirements.txt             # Dependencias Python
├── .env.example                 # Template de variables de entorno
├── .gitignore                   # Archivos ignorados por Git
├── create_admin.py              # Script: Crear superadmin
├── manage_users.py              # Script: Gestión de usuarios CLI
│
├── README.md                    # Este archivo
├── MULTIUSUARIO_README.md       # Guía multiusuario
├── PWA_README.md                # Guía PWA
├── ADMIN_APP_STYLE_GUIDE.md     # Guía de diseño panel control
└── SECURITY_ADMIN_APP.md        # Documentación de seguridad
```

---

## 📚 Documentación Adicional

- **[MULTIUSUARIO_README.md](MULTIUSUARIO_README.md):** Guía detallada del sistema multiusuario
- **[PWA_README.md](PWA_README.md):** Configuración y uso como Progressive Web App
- **[ADMIN_APP_STYLE_GUIDE.md](ADMIN_APP_STYLE_GUIDE.md):** Guía de diseño del panel de control
- **[SECURITY_ADMIN_APP.md](SECURITY_ADMIN_APP.md):** Medidas de seguridad implementadas

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Este es un proyecto de código abierto diseñado para la comunidad.

### Cómo Contribuir

1. **Fork** el repositorio
2. **Crea** una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add: Amazing Feature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. **Abre** un Pull Request

### Guías de Estilo

- **Python:** Sigue PEP 8
- **JavaScript:** Usa ESLint con Airbnb style guide
- **CSS:** BEM methodology para clases
- **Commits:** Conventional Commits (feat:, fix:, docs:, style:, refactor:, test:, chore:)

### Reportar Bugs

Abre un [issue](https://github.com/cdavidg/Tag2QR/issues) con:
- Descripción clara del bug
- Pasos para reproducir
- Comportamiento esperado vs actual
- Screenshots si aplica
- Entorno (OS, Python version, navegador)

### Solicitar Features

Abre un [issue](https://github.com/cdavidg/Tag2QR/issues) con:
- Descripción detallada del feature
- Casos de uso
- Mockups o ejemplos (opcional)

---

## 🔮 Roadmap

### v1.1 (Próxima versión)
- [ ] Integración con APIs de e-commerce (WooCommerce, Shopify)
- [ ] Exportación de inventario (CSV, Excel)
- [ ] Modo multidioma (i18n)
- [ ] Notificaciones push por bajo stock
- [ ] Historial de cambios de precio

### v2.0 (Futuro)
- [ ] Dashboard de ventas integrado
- [ ] Generación de reportes PDF
- [ ] API REST para integraciones
- [ ] Soporte para PostgreSQL
- [ ] Sistema de roles personalizable
- [ ] Multi-sucursal por tienda
- [ ] Integración con impresoras térmicas
- [ ] App móvil nativa (React Native)

---

## 📄 Licencia

Este proyecto está licenciado bajo la **Licencia MIT** - ver el archivo [LICENSE](LICENSE) para más detalles.

```
MIT License

Copyright (c) 2025 David García

Se concede permiso, de forma gratuita, a cualquier persona que obtenga una copia
de este software y de los archivos de documentación asociados (el "Software"), 
para utilizar el Software sin restricción, incluyendo sin limitación los derechos 
a usar, copiar, modificar, fusionar, publicar, distribuir, sublicenciar, y/o vender 
copias del Software.
```

---

## 👨‍💻 Autor

**David García**
- GitHub: [@cdavidg](https://github.com/cdavidg)
- Email: cedav95@gmail.com
- Website: [tag2qr.shop](https://tag2qr.shop)

---

## 🙏 Agradecimientos

- A la comunidad de Flask por un framework increíble
- A todos los contribuidores de las librerías open source utilizadas
- A la comunidad de desarrolladores que hacen posible el software libre

---

## 📞 Soporte

¿Tienes preguntas? ¿Necesitas ayuda?

- 📧 Email: cedav95@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/cdavidg/Tag2QR/issues)
- 💬 Discusiones: [GitHub Discussions](https://github.com/cdavidg/Tag2QR/discussions)

---

<div align="center">

**⭐ Si este proyecto te resulta útil, considera darle una estrella en GitHub ⭐**

Made with ❤️ for the Open Source Community

</div>
