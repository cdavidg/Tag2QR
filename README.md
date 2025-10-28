<!-- Multilingual README: English, Arabic, Spanish -->
# 🏷️ Tag2QR — Dynamic QR Product Management System

<div align="center">

![Tag2QR](https://img.shields.io/badge/Tag2QR-v1.0-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![Python](https://img.shields.io/badge/Python-3.8+-yellow)
![License](https://img.shields.io/badge/License-MIT-red)

This repository contains Tag2QR, a Progressive Web App (PWA) that converts physical product tags into dynamic QR codes linked to a live product database.

[🌐 Demo](https://tag2qr.shop) • [📖 Documentation](#documentation) • [🚀 Installation](#quick-install-developer) • [💡 Features](#features)

</div>

---

## English

### 📋 Table of Contents

- [What is Tag2QR?](#what-is-tag2qr-en)
- [Key Features](#key-features-en)
- [Use Cases](#use-cases-en)
- [System Architecture](#system-architecture-en)
- [Installation](#installation-en)
- [Configuration](#configuration-en)
- [User Guide](#user-guide-en)
- [Technologies](#technologies-en)
- [Project Structure](#project-structure-en)
- [Additional Documentation](#additional-documentation-en)
- [Contributing](#contributing-en)
- [License](#license-en)

---

<a id="what-is-tag2qr-en"></a>
### 🎯 What is Tag2QR?

**Tag2QR** is a Progressive Web Application (PWA) that revolutionizes product management through dynamic QR codes. Instead of printing labels with static information that becomes outdated, Tag2QR generates QR codes that link directly to your database, displaying **always up-to-date** information when scanned.

#### 💡 The Problem It Solves

- ❌ **Traditional labels:** Printed price → Price change → Reprint label → Cost and waste
- ✅ **Tag2QR:** Printed QR code → Price change in system → QR shows new price → No reprinting

---

<a id="key-features-en"></a>
### ✨ Key Features

#### 🛍️ For Stores and Businesses

- **Instant Updates:** Modify prices, descriptions or stock and changes are immediately reflected when scanning the QR
- **Multiple Stores:** Multi-user system with support for multiple independent businesses
- **No Reprinting:** Print the QR once and update information infinitely
- **Total Customization:** Logo, colors, information displayed on labels and public pages
- **Inventory Management:** Stock control, categories, images and detailed descriptions

#### 📱 Customer Experience

- **Quick Scanning:** Any QR reader app (smartphone camera)
- **Complete Information:** Price, description, availability, product images
- **No Apps Required:** Works directly in browser
- **Responsive:** Design optimized for mobile, tablets and desktop
- **PWA:** Installable as native app on mobile devices

#### 👨‍💼 Admin Panel

**Store Panel (`/admin`) - Regular Users:**
- **Dashboard:** Product statistics, inventory value, best-selling products
- **Product Management:** Full CRUD (create, read, update, delete)
- **Categories:** Organization by custom categories
- **QR Generation:**
  - Individual QR per product
  - Bulk QR with batch download
  - Printable labels with custom logo and design
- **Code Scanner:** Integrated QR/barcode reader for quick search
- **Store Configuration:** Logo, contact information, label templates
- **User Management:** (Store admins only)

**Control Panel (`/admin_app`) - Superadministrators:**
- **Global User Management:** Create, edit, delete system users
- **Global Product Management:** Complete view of products from all stores
- **Store Management:** Administer configurations of all stores
- **Global Statistics:** System-wide metrics
- **Dark Mode Design:** WordPress-style interface with professional dark theme
- **Multi-Layer Security:** Authentication, authorization and validation on each request

#### 🎨 Label Customization

- **Available Templates:** Rectangular, square, circular
- **Configurable Elements:**
  - Show/hide: Logo, store name, product name, price, SKU, description
  - Customizable font size
  - Colors: Background, text, border
  - Dimensions: Width, height, padding, QR size
  - Border styles

#### 🔧 Technical Features

- **PWA (Progressive Web App):** Works offline, installable, push notifications
- **Multi-user:** Each user has their own isolated store
- **Access Levels:** User, Administrator, Superadministrator
- **SQLite Database:** Lightweight, no external server, easy to backup
- **Image Upload:** Support for multiple images per product
- **On-the-fly QR Generation:** QRs are dynamically generated based on configuration
- **Responsive Design:** Modern CSS with flexbox and grid
- **Font Awesome 6.4.0:** Professional iconography
- **Session Management:** Session persistence with Flask-Login

---

<a id="use-cases-en"></a>
### 💼 Use Cases

#### 🏪 Retail Stores
- Price labels on shelves
- Product information without physical space
- Real-time offer/discount updates

#### 📦 Warehouses and Logistics
- Product tracking
- Location information
- Inventory control

#### 🍽️ Restaurants and Cafes
- Updateable digital menus
- Nutritional information and allergens
- Seasonal prices

#### 🏭 Industry and Manufacturing
- Technical product specifications
- Linked user manuals
- Warranty information

#### 🎨 Galleries and Museums
- Artwork information
- Linked audio guides
- Artist biographies

#### 🏨 Hotels and Tourism
- Service information
- Maps and directions
- Tour prices

---

<a id="system-architecture-en"></a>
### 🏗️ System Architecture

```
Tag2QR
│
├── Frontend (Responsive HTML5/CSS3/JS)
│   ├── Public Interface (QR Scan Results)
│   ├── Admin Panel (Store Management)
│   └── Control Panel (Super Admin)
│
├── Backend (Flask 3.0 + Python 3.12)
│   ├── Blueprints:
│   │   ├── auth_bp (Authentication)
│   │   ├── admin_bp (Store panel)
│   │   ├── admin_app_bp (Control panel)
│   │   ├── store_bp (Store configuration)
│   │   ├── category_bp (Categories)
│   │   ├── qr_bp (QR Generation)
│   │   └── public_bp (Public pages)
│   │
│   ├── Models (SQLAlchemy ORM):
│   │   ├── User (Users + Auth)
│   │   ├── Store (Store configuration)
│   │   ├── Product (Products)
│   │   └── Category (Categories)
│   │
│   └── Security:
│       ├── @login_required
│       ├── @admin_required
│       └── @superadmin_required
│
├── Database (SQLite)
│   └── shopqr.db (Normalized relational)
│
└── Storage
    ├── uploads/products/ (Images)
    ├── uploads/qr/ (Generated QRs)
    └── uploads/store/ (Logos)
```

#### 📊 Data Model

```
User
├── id, email, password_hash
├── name, is_admin, is_superadmin
└── Relations: Store (1:1), Products (1:N)

Store
├── id, user_id, name, phone, email
├── logo_filename, address, website
├── label_* (Label configuration)
└── Relation: User (N:1)

Product
├── id, user_id, name, sku, barcode
├── description, price, stock, cost
├── category_id, images_json
└── Relations: User (N:1), Category (N:1)

Category
├── id, user_id, name, description
└── Relations: User (N:1), Products (1:N)
```

---

<a id="installation-en"></a>
### 🚀 Installation

#### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

#### Step 1: Clone Repository

```bash
git clone https://github.com/cdavidg/Tag2QR.git
cd Tag2QR
```

#### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 4: Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your configurations:

```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-very-secure-secret-key-here
DATABASE_URL=sqlite:///instance/shopqr.db
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216  # 16MB
```

#### Step 5: Initialize Database

```bash
flask db upgrade  # If using migrations
# Or simply run the app (will create DB automatically)
python app.py
```

#### Step 6: Create Admin User

```bash
python create_admin.py
```

Follow instructions to create your first superadministrator.

#### Step 7: Run Application

```bash
# Development mode
python app.py

# Production mode (with Gunicorn)
gunicorn -w 3 -b 127.0.0.1:8000 app:app
```

Application will be available at `http://localhost:5000` (development) or `http://localhost:8000` (production).

---

<a id="configuration-en"></a>
### ⚙️ Configuration

#### Environment Variables

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `FLASK_APP` | Entry file | `app.py` |
| `FLASK_ENV` | Runtime environment | `production` |
| `SECRET_KEY` | Flask secret key | *Required* |
| `DATABASE_URL` | Database URL | `sqlite:///instance/shopqr.db` |
| `UPLOAD_FOLDER` | Upload directory | `uploads` |
| `MAX_CONTENT_LENGTH` | Maximum file size | `16777216` (16MB) |

#### Production Configuration

For production environments, recommended:

1. **WSGI Server:** Gunicorn, uWSGI
2. **Reverse Proxy:** Nginx, Apache
3. **HTTPS:** SSL/TLS Certificate (Let's Encrypt)
4. **Database:** Migrate to PostgreSQL or MySQL for high traffic
5. **Storage:** AWS S3 or similar for images
6. **Backups:** Automate DB and uploads backups

---

<a id="user-guide-en"></a>
### 📖 User Guide

#### 🔐 System Access

**For Users/Stores:**
1. **Registration:** Superadministrator creates your account from `/admin_app`
2. **Login:** Access at `https://yourdomain.com/admin/login`
3. **Initial Setup:**
   - Go to "Store Configuration"
   - Upload your logo
   - Complete contact information
   - Configure label template

**For Superadministrators:**
1. **Create Superadmin:**
   ```bash
   python create_admin.py
   ```
2. **Login:** Access at `https://yourdomain.com/admin/login`
3. **Access Control Panel:**
   - A "👑 Control Panel" button will appear in user menu
   - You can also access directly at `https://yourdomain.com/admin_app`

#### 🛒 Product Management

**Create Product:**
1. Admin Panel → "New Product"
2. Complete fields:
   - **Name:** Product title
   - **SKU:** Unique code (optional, auto-generated)
   - **Barcode:** For scanner reading
   - **Category:** Select or create new
   - **Price:** Sale price
   - **Cost:** Acquisition cost (optional)
   - **Stock:** Available quantity
   - **Description:** Detailed text (supports markdown)
   - **Images:** Up to 5 images
3. Save

**Generate QR:**
- **Individual QR:** Go to product detail → "Generate QR" → Download PNG
- **Bulk QR:** Panel → "Labels" → Select products (checkbox) → "Generate Selected Labels" → Download PDF
- **Configure Design:** Panel → "Store Configuration" → "Label Templates" → Adjust settings → Save

#### 🔍 Product Scanner

Built-in scanner allows quick product search:
1. Panel → "Scanner" (camera icon)
2. Allow camera access
3. Focus on barcode or QR
4. Automatic result: Product found → Show details and stock / Not found → Option to create new product

---

<a id="technologies-en"></a>
### 🛠️ Technologies

**Backend:**
- Flask 3.0.0, Flask-SQLAlchemy 3.1.1, Flask-Login 0.6.3, Flask-WTF 1.2.1
- Flask-Migrate 4.0.5, Werkzeug 3.0.1, qrcode[pil] 7.4.2, Pillow 10.0+

**Frontend:**
- HTML5, CSS3 (Flexbox, Grid), JavaScript Vanilla, Font Awesome 6.4.0
- html5-qrcode, Service Worker

**Database:**
- SQLite (development), PostgreSQL/MySQL (production)

---

<a id="project-structure-en"></a>
### 📁 Project Structure

```
Tag2QR/
├── app/ (Application modules)
├── templates/ (Jinja2 templates)
├── static/ (CSS, JS, icons, PWA files)
├── uploads/ (Uploaded files - not in Git)
├── instance/ (App instance - not in Git)
├── app.py, config.py, requirements.txt
└── README.md, documentation files
```

---

<a id="additional-documentation-en"></a>
### 📚 Additional Documentation

- **MULTIUSUARIO_README.md:** Detailed multi-user system guide
- **PWA_README.md:** Progressive Web App configuration and usage
- **ADMIN_APP_STYLE_GUIDE.md:** Control panel design guide
- **SECURITY_ADMIN_APP.md:** Implemented security measures

---

<a id="contributing-en"></a>
### 🤝 Contributing

Contributions are welcome! This is an open source project designed for the community.

**How to Contribute:**
1. **Fork** the repository
2. **Create** a branch for your feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add: Amazing Feature'`)
4. **Push** to branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

**Report Bugs:** Open an [issue](https://github.com/cdavidg/Tag2QR/issues) with description, steps to reproduce, expected vs actual behavior, screenshots, environment details.

**Request Features:** Open an [issue](https://github.com/cdavidg/Tag2QR/issues) with detailed description, use cases, mockups.

---

<a id="license-en"></a>
### 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

```
MIT License
Copyright (c) 2025 David García
Permission is granted, free of charge, to any person obtaining a copy...
```

---

### 👨‍💻 Author

**David García**
- GitHub: [@cdavidg](https://github.com/cdavidg)
- Email: cedav95@gmail.com
- Website: [tag2qr.shop](https://tag2qr.shop)

---

### 📞 Support

Questions? Need help?
- 📧 Email: cedav95@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/cdavidg/Tag2QR/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/cdavidg/Tag2QR/discussions)

---

<div align="center">

**⭐ If you find this project useful, consider giving it a star on GitHub ⭐**

Made with ❤️ for the Open Source Community

</div>

---

## العربية (Arabic)

### 📋 جدول المحتويات

- [ما هو Tag2QR؟](#ما-هو-tag2qr-ar)
- [الميزات الرئيسية](#الميزات-الرئيسية-ar)
- [حالات الاستخدام](#حالات-الاستخدام-ar)
- [بنية النظام](#بنية-النظام-ar)
- [التثبيت](#التثبيت-ar)
- [الإعداد](#الإعداد-ar)
- [دليل المستخدم](#دليل-المستخدم-ar)
- [التقنيات](#التقنيات-ar)
- [هيكل المشروع](#هيكل-المشروع-ar)
- [الوثائق الإضافية](#الوثائق-الإضافية-ar)
- [المساهمة](#المساهمة-ar)
- [الترخيص](#الترخيص-ar)

---

<a id="ما-هو-tag2qr-ar"></a>
### 🎯 ما هو Tag2QR؟

**Tag2QR** هو تطبيق ويب تقدمي (PWA) يُحدث ثورة في إدارة المنتجات من خلال رموز QR الديناميكية. بدلاً من طباعة الملصقات بمعلومات ثابتة تصبح قديمة، يُنشئ Tag2QR رموز QR ترتبط مباشرة بقاعدة البيانات الخاصة بك، وتعرض معلومات **محدثة دائمًا** عند المسح.

#### 💡 المشكلة التي يحلها

- ❌ **الملصقات التقليدية:** سعر مطبوع → تغيير السعر → إعادة طباعة الملصق → تكلفة وهدر
- ✅ **Tag2QR:** رمز QR مطبوع → تغيير السعر في النظام → يظهر QR السعر الجديد → بدون إعادة طباعة

---

<a id="الميزات-الرئيسية-ar"></a>
### ✨ الميزات الرئيسية

#### 🛍️ للمتاجر والأعمال

- **تحديثات فورية:** تعديل الأسعار أو الأوصاف أو المخزون وتنعكس التغييرات فورًا عند مسح رمز QR
- **متاجر متعددة:** نظام متعدد المستخدمين مع دعم لأعمال مستقلة متعددة
- **بدون إعادة طباعة:** اطبع رمز QR مرة واحدة وحدّث المعلومات بلا حدود
- **تخصيص كامل:** شعار، ألوان، معلومات معروضة على الملصقات والصفحات العامة
- **إدارة المخزون:** التحكم في المخزون، الفئات، الصور والأوصاف التفصيلية

#### 📱 تجربة العميل

- **مسح سريع:** أي تطبيق قارئ QR (كاميرا الهاتف الذكي)
- **معلومات كاملة:** السعر، الوصف، التوفر، صور المنتج
- **لا حاجة لتطبيقات:** يعمل مباشرة في المتصفح
- **متجاوب:** تصميم محسّن للهواتف المحمولة والأجهزة اللوحية وسطح المكتب
- **PWA:** قابل للتثبيت كتطبيق أصلي على الأجهزة المحمولة

#### 👨‍💼 لوحة الإدارة

**لوحة المتجر (`/admin`) - المستخدمون العاديون:**
- **لوحة المعلومات:** إحصائيات المنتجات، قيمة المخزون، المنتجات الأكثر مبيعًا
- **إدارة المنتجات:** CRUD كامل (إنشاء، قراءة، تحديث، حذف)
- **الفئات:** تنظيم حسب فئات مخصصة
- **إنشاء QR:**
  - QR فردي لكل منتج
  - QR جماعي مع تنزيل دفعي
  - ملصقات قابلة للطباعة مع شعار وتصميم مخصص
- **ماسح الأكواد:** قارئ QR/باركود متكامل للبحث السريع
- **إعداد المتجر:** الشعار، معلومات الاتصال، قوالب الملصقات
- **إدارة المستخدمين:** (مسؤولو المتجر فقط)

**لوحة التحكم (`/admin_app`) - المشرفون العامون:**
- **إدارة المستخدمين العامة:** إنشاء، تحرير، حذف مستخدمي النظام
- **إدارة المنتجات العامة:** عرض كامل لمنتجات جميع المتاجر
- **إدارة المتاجر:** إدارة إعدادات جميع المتاجر
- **إحصاءات عامة:** مقاييس على مستوى النظام
- **تصميم الوضع الداكن:** واجهة بنمط WordPress مع ثيم داكن احترافي
- **أمان متعدد الطبقات:** مصادقة، تفويض والتحقق في كل طلب

#### 🎨 تخصيص الملصقات

- **القوالب المتاحة:** مستطيل، مربع، دائري
- **العناصر القابلة للتكوين:**
  - إظهار/إخفاء: الشعار، اسم المتجر، اسم المنتج، السعر، SKU، الوصف
  - حجم الخط قابل للتخصيص
  - الألوان: الخلفية، النص، الحدود
  - الأبعاد: العرض، الارتفاع، الحشو، حجم QR
  - أنماط الحدود

#### 🔧 الميزات التقنية

- **PWA (تطبيق ويب تقدمي):** يعمل دون اتصال، قابل للتثبيت، إشعارات الدفع
- **متعدد المستخدمين:** لكل مستخدم متجره المعزول الخاص
- **مستويات الوصول:** مستخدم، مسؤول، مشرف عام
- **قاعدة بيانات SQLite:** خفيفة، بدون خادم خارجي، سهلة النسخ الاحتياطي
- **تحميل الصور:** دعم لصور متعددة لكل منتج
- **إنشاء QR في الحال:** يتم إنشاء رموز QR ديناميكيًا بناءً على الإعداد
- **تصميم متجاوب:** CSS حديث مع flexbox و grid
- **Font Awesome 6.4.0:** أيقونات احترافية
- **إدارة الجلسات:** استمرارية الجلسة مع Flask-Login

---

<a id="حالات-الاستخدام-ar"></a>
### 💼 حالات الاستخدام

#### 🏪 متاجر التجزئة
- ملصقات الأسعار على الأرفف
- معلومات المنتج بدون مساحة فعلية
- تحديثات العروض/الخصومات في الوقت الفعلي

#### 📦 المستودعات واللوجستيات
- تتبع المنتجات
- معلومات الموقع
- التحكم في المخزون

#### 🍽️ المطاعم والمقاهي
- قوائم رقمية قابلة للتحديث
- المعلومات الغذائية ومسببات الحساسية
- أسعار موسمية

#### 🏭 الصناعة والتصنيع
- المواصفات الفنية للمنتجات
- أدلة الاستخدام المرتبطة
- معلومات الضمان

#### 🎨 المعارض والمتاحف
- معلومات الأعمال الفنية
- أدلة صوتية مرتبطة
- سير ذاتية للفنانين

#### 🏨 الفنادق والسياحة
- معلومات الخدمات
- الخرائط والاتجاهات
- أسعار الرحلات

---

<a id="بنية-النظام-ar"></a>
### 🏗️ بنية النظام

```
Tag2QR
│
├── الواجهة الأمامية (HTML5/CSS3/JS متجاوب)
│   ├── الواجهة العامة (نتائج مسح QR)
│   ├── لوحة الإدارة (إدارة المتجر)
│   └── لوحة التحكم (مشرف عام)
│
├── الخلفية (Flask 3.0 + Python 3.12)
│   ├── Blueprints:
│   │   ├── auth_bp (المصادقة)
│   │   ├── admin_bp (لوحة المتجر)
│   │   ├── admin_app_bp (لوحة التحكم)
│   │   ├── store_bp (إعداد المتجر)
│   │   ├── category_bp (الفئات)
│   │   ├── qr_bp (إنشاء QR)
│   │   └── public_bp (الصفحات العامة)
│   │
│   ├── النماذج (SQLAlchemy ORM):
│   │   ├── User (المستخدمون + المصادقة)
│   │   ├── Store (إعداد المتجر)
│   │   ├── Product (المنتجات)
│   │   └── Category (الفئات)
│   │
│   └── الأمان:
│       ├── @login_required
│       ├── @admin_required
│       └── @superadmin_required
│
├── قاعدة البيانات (SQLite)
│   └── shopqr.db (علائقية موحدة)
│
└── التخزين
    ├── uploads/products/ (الصور)
    ├── uploads/qr/ (رموز QR المُنشأة)
    └── uploads/store/ (الشعارات)
```

#### 📊 نموذج البيانات

```
User
├── id, email, password_hash
├── name, is_admin, is_superadmin
└── العلاقات: Store (1:1), Products (1:N)

Store
├── id, user_id, name, phone, email
├── logo_filename, address, website
├── label_* (إعداد الملصق)
└── العلاقة: User (N:1)

Product
├── id, user_id, name, sku, barcode
├── description, price, stock, cost
├── category_id, images_json
└── العلاقات: User (N:1), Category (N:1)

Category
├── id, user_id, name, description
└── العلاقات: User (N:1), Products (1:N)
```

---

<a id="التثبيت-ar"></a>
### 🚀 التثبيت

#### المتطلبات الأساسية

- Python 3.8 أو أحدث
- pip (مدير حزم Python)
- Git

#### الخطوة 1: استنساخ المستودع

```bash
git clone https://github.com/cdavidg/Tag2QR.git
cd Tag2QR
```

#### الخطوة 2: إنشاء بيئة افتراضية

```bash
python3 -m venv venv
source venv/bin/activate  # على Windows: venv\\Scripts\\activate
```

#### الخطوة 3: تثبيت التبعيات

```bash
pip install -r requirements.txt
```

#### الخطوة 4: إعداد متغيرات البيئة

```bash
cp .env.example .env
```

حرر `.env` بإعداداتك:

```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=مفتاحك-السري-الآمن-جدًا-هنا
DATABASE_URL=sqlite:///instance/shopqr.db
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216  # 16MB
```

#### الخطوة 5: تهيئة قاعدة البيانات

```bash
flask db upgrade  # إذا كنت تستخدم الترحيلات
# أو ببساطة قم بتشغيل التطبيق (سينشئ قاعدة البيانات تلقائيًا)
python app.py
```

#### الخطوة 6: إنشاء مستخدم مسؤول

```bash
python create_admin.py
```

اتبع التعليمات لإنشاء أول مشرف عام لك.

#### الخطوة 7: تشغيل التطبيق

```bash
# وضع التطوير
python app.py

# وضع الإنتاج (مع Gunicorn)
gunicorn -w 3 -b 127.0.0.1:8000 app:app
```

سيكون التطبيق متاحًا على `http://localhost:5000` (تطوير) أو `http://localhost:8000` (إنتاج).

---

<a id="الإعداد-ar"></a>
### ⚙️ الإعداد

#### متغيرات البيئة

| المتغير | الوصف | القيمة الافتراضية |
|---------|-------|-------------------|
| `FLASK_APP` | ملف الإدخال | `app.py` |
| `FLASK_ENV` | بيئة التشغيل | `production` |
| `SECRET_KEY` | مفتاح Flask السري | *مطلوب* |
| `DATABASE_URL` | عنوان قاعدة البيانات | `sqlite:///instance/shopqr.db` |
| `UPLOAD_FOLDER` | دليل التحميلات | `uploads` |
| `MAX_CONTENT_LENGTH` | الحد الأقصى لحجم الملف | `16777216` (16MB) |

#### إعداد الإنتاج

لبيئات الإنتاج، يُوصى بـ:

1. **خادم WSGI:** Gunicorn، uWSGI
2. **وكيل عكسي:** Nginx، Apache
3. **HTTPS:** شهادة SSL/TLS (Let's Encrypt)
4. **قاعدة البيانات:** الانتقال إلى PostgreSQL أو MySQL لحركة المرور العالية
5. **التخزين:** AWS S3 أو ما شابه للصور
6. **النسخ الاحتياطية:** أتمتة النسخ الاحتياطية لقاعدة البيانات والتحميلات

---

<a id="دليل-المستخدم-ar"></a>
### 📖 دليل المستخدم

#### 🔐 الوصول إلى النظام

**للمستخدمين/المتاجر:**
1. **التسجيل:** ينشئ المشرف العام حسابك من `/admin_app`
2. **تسجيل الدخول:** الوصول على `https://yourdomain.com/admin/login`
3. **الإعداد الأولي:**
   - انتقل إلى "إعداد المتجر"
   - قم بتحميل شعارك
   - أكمل معلومات الاتصال
   - قم بإعداد قالب الملصق

**للمشرفين العامين:**
1. **إنشاء مشرف عام:**
   ```bash
   python create_admin.py
   ```
2. **تسجيل الدخول:** الوصول على `https://yourdomain.com/admin/login`
3. **الوصول إلى لوحة التحكم:**
   - سيظهر زر "👑 لوحة التحكم" في قائمة المستخدم
   - يمكنك أيضًا الوصول مباشرة إلى `https://yourdomain.com/admin_app`

#### 🛒 إدارة المنتجات

**إنشاء منتج:**
1. لوحة الإدارة → "منتج جديد"
2. أكمل الحقول:
   - **الاسم:** عنوان المنتج
   - **SKU:** كود فريد (اختياري، يتم إنشاؤه تلقائيًا)
   - **الباركود:** لقراءة الماسح الضوئي
   - **الفئة:** حدد أو أنشئ جديدة
   - **السعر:** سعر البيع
   - **التكلفة:** تكلفة الشراء (اختياري)
   - **المخزون:** الكمية المتاحة
   - **الوصف:** نص تفصيلي (يدعم markdown)
   - **الصور:** حتى 5 صور
3. حفظ

**إنشاء QR:**
- **QR فردي:** انتقل إلى تفاصيل المنتج → "إنشاء QR" → تنزيل PNG
- **QR جماعي:** اللوحة → "الملصقات" → حدد المنتجات (خانة الاختيار) → "إنشاء ملصقات محددة" → تنزيل PDF
- **إعداد التصميم:** اللوحة → "إعداد المتجر" → "قوالب الملصقات" → ضبط الإعدادات → حفظ

#### 🔍 ماسح المنتجات

يتيح الماسح المدمج البحث السريع عن المنتجات:
1. اللوحة → "الماسح" (أيقونة الكاميرا)
2. السماح بالوصول إلى الكاميرا
3. ركّز على الباركود أو QR
4. النتيجة التلقائية: تم العثور على المنتج → إظهار التفاصيل والمخزون / لم يتم العثور عليه → خيار إنشاء منتج جديد

---

<a id="التقنيات-ar"></a>
### 🛠️ التقنيات

**الخلفية:**
- Flask 3.0.0، Flask-SQLAlchemy 3.1.1، Flask-Login 0.6.3، Flask-WTF 1.2.1
- Flask-Migrate 4.0.5، Werkzeug 3.0.1، qrcode[pil] 7.4.2، Pillow 10.0+

**الواجهة الأمامية:**
- HTML5، CSS3 (Flexbox، Grid)، JavaScript Vanilla، Font Awesome 6.4.0
- html5-qrcode، Service Worker

**قاعدة البيانات:**
- SQLite (التطوير)، PostgreSQL/MySQL (الإنتاج)

---

<a id="هيكل-المشروع-ar"></a>
### 📁 هيكل المشروع

```
Tag2QR/
├── app/ (وحدات التطبيق)
├── templates/ (قوالب Jinja2)
├── static/ (CSS، JS، الأيقونات، ملفات PWA)
├── uploads/ (الملفات المحملة - ليست في Git)
├── instance/ (نسخة التطبيق - ليست في Git)
├── app.py, config.py, requirements.txt
└── README.md، ملفات التوثيق
```

---

<a id="الوثائق-الإضافية-ar"></a>
### 📚 الوثائق الإضافية

- **MULTIUSUARIO_README.md:** دليل مفصل لنظام متعدد المستخدمين
- **PWA_README.md:** إعداد واستخدام تطبيق الويب التقدمي
- **ADMIN_APP_STYLE_GUIDE.md:** دليل تصميم لوحة التحكم
- **SECURITY_ADMIN_APP.md:** إجراءات الأمان المطبقة

---

<a id="المساهمة-ar"></a>
### 🤝 المساهمة

المساهمات مرحب بها! هذا مشروع مفتوح المصدر مصمم للمجتمع.

**كيفية المساهمة:**
1. **Fork** المستودع
2. **إنشاء** فرع لميزتك (`git checkout -b feature/AmazingFeature`)
3. **Commit** تغييراتك (`git commit -m 'Add: Amazing Feature'`)
4. **Push** إلى الفرع (`git push origin feature/AmazingFeature`)
5. **فتح** Pull Request

**الإبلاغ عن الأخطاء:** افتح [issue](https://github.com/cdavidg/Tag2QR/issues) مع الوصف، خطوات إعادة الإنتاج، السلوك المتوقع مقابل الفعلي، لقطات الشاشة، تفاصيل البيئة.

**طلب ميزات:** افتح [issue](https://github.com/cdavidg/Tag2QR/issues) مع وصف تفصيلي، حالات الاستخدام، نماذج بالحجم الطبيعي.

---

<a id="الترخيص-ar"></a>
### 📄 الترخيص

هذا المشروع مرخص بموجب **ترخيص MIT** - انظر ملف [LICENSE](LICENSE) للتفاصيل.

```
ترخيص MIT
حقوق النشر (c) 2025 ديفيد غارسيا
يُمنح الإذن، مجانًا، لأي شخص يحصل على نسخة...
```

---

### 👨‍💻 المؤلف

**ديفيد غارسيا**
- GitHub: [@cdavidg](https://github.com/cdavidg)
- البريد الإلكتروني: cedav95@gmail.com
- الموقع الإلكتروني: [tag2qr.shop](https://tag2qr.shop)

---

### 📞 الدعم

أسئلة؟ تحتاج مساعدة؟
- 📧 البريد الإلكتروني: cedav95@gmail.com
- 🐛 المشاكل: [GitHub Issues](https://github.com/cdavidg/Tag2QR/issues)
- 💬 المناقشات: [GitHub Discussions](https://github.com/cdavidg/Tag2QR/discussions)

---

<div align="center">

**⭐ إذا وجدت هذا المشروع مفيدًا، ففكر في منحه نجمة على GitHub ⭐**

صُنع بـ ❤️ لمجتمع المصادر المفتوحة

</div>

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

<a id="documentation"></a>
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
