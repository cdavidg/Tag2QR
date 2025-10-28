# 📂 Análisis de Estructura del Proyecto Tag2QR

## 🔍 Estado Actual de Directorios

### Directorio `/var/www/vhosts/tag2qr.shop/httpdocs/` (PRODUCCIÓN ACTIVA)

**Status:** ✅ **En uso - Versión de producción**

Este es el directorio activo en producción. Contiene:

- **Código actualizado** con todas las características implementadas:
  - Sistema multiusuario completo
  - Panel de administración (`/admin`)
  - Panel de control superadmin (`/admin_app`)
  - PWA funcional
  - Escáner de códigos integrado
  - Generación de QR dinámicos
  - Gestión de inventario

- **Archivos adicionales de producción:**
  - `admin_app.py` - Blueprint del panel de control
  - `migrate_superadmin.py` - Script de migración de DB
  - `passenger_wsgi.py` / `wsgi.py` - Configuración para despliegue
  - Documentación completa (ADMIN_APP_STYLE_GUIDE.md, SECURITY_ADMIN_APP.md, etc.)

- **Base de datos activa:**
  - `instance/shopqr.db` con datos reales de producción
  - Usuarios registrados
  - Productos y tiendas activas

- **Uploads con contenido:**
  - `uploads/products/` - Imágenes de productos reales
  - `uploads/qr/` - QR generados
  - `uploads/store/` - Logos de tiendas

### Directorio `/var/www/vhosts/tag2qr.shop/tag2qr/` (OBSOLETO)

**Status:** ⚠️ **Duplicado desactualizado - Puede eliminarse**

Este directorio contiene una versión anterior del código:

- **NO está en uso** por el servicio `tag2qr.service`
- **NO tiene las últimas características:**
  - ❌ Falta `admin_app.py` (panel de control)
  - ❌ Código de auth.py, admin.py, models.py desactualizados
  - ❌ No tiene documentación reciente
  - ❌ No tiene archivos de migración de superadmin

- **Archivos útiles a preservar:**
  - `.env.example` (ya copiado a httpdocs)
  - `.gitignore` (ya copiado a httpdocs)
  - Posible backup de configuración antigua

## 📊 Comparación de Versiones

| Característica | `/httpdocs` (Producción) | `/tag2qr` (Obsoleto) |
|----------------|--------------------------|----------------------|
| En uso por servicio | ✅ Sí | ❌ No |
| Panel de Control (admin_app) | ✅ | ❌ |
| Campo is_superadmin | ✅ | ❌ |
| Documentación completa | ✅ | ⚠️ Parcial |
| Código actualizado | ✅ | ❌ |
| Base de datos activa | ✅ | ⚠️ Antigua |
| Uploads reales | ✅ | ⚠️ Antiguos |

## 🎯 Recomendaciones

### Opción 1: Eliminar `/tag2qr` (RECOMENDADO)

**✅ Pros:**
- Elimina confusión sobre cuál es la versión activa
- Libera espacio en disco
- Simplifica la estructura del proyecto
- Evita editar archivos incorrectos por error

**❌ Cons:**
- Se pierde backup local (mitigable con Git)

**Pasos:**
```bash
# 1. Verificar que no hay archivos únicos importantes
diff -rq /var/www/vhosts/tag2qr.shop/tag2qr /var/www/vhosts/tag2qr.shop/httpdocs

# 2. Hacer backup final (opcional)
tar -czf /var/www/vhosts/tag2qr.shop/tag2qr_backup_$(date +%Y%m%d).tar.gz /var/www/vhosts/tag2qr.shop/tag2qr/

# 3. Eliminar directorio
rm -rf /var/www/vhosts/tag2qr.shop/tag2qr/
```

### Opción 2: Mantener como Backup (TEMPORAL)

Si prefieres mantenerlo temporalmente:

```bash
# Renombrar para claridad
mv /var/www/vhosts/tag2qr.shop/tag2qr /var/www/vhosts/tag2qr.shop/tag2qr_OLD_BACKUP

# Documentar que no está en uso
echo "OBSOLETO - NO USAR - Backup antiguo" > /var/www/vhosts/tag2qr.shop/tag2qr_OLD_BACKUP/README_OBSOLETE.txt
```

### Opción 3: Sincronizar Selectivamente (NO RECOMENDADO)

**⚠️ Riesgo de sobrescribir código actualizado**

No se recomienda copiar archivos de `/tag2qr` a `/httpdocs` porque:
- Los archivos en httpdocs son más recientes
- Podrías perder las características implementadas
- Mayor riesgo de introducir bugs

## 🗂️ Estructura Recomendada Final

```
/var/www/vhosts/tag2qr.shop/
│
├── httpdocs/                    # ✅ PRODUCCIÓN ACTIVA
│   ├── app/                     # Código fuente
│   ├── templates/               # Plantillas
│   ├── static/                  # Archivos estáticos
│   ├── uploads/                 # Uploads (no en Git)
│   ├── instance/                # Base de datos (no en Git)
│   ├── venv/                    # Entorno virtual (no en Git)
│   ├── .env                     # Variables de entorno (no en Git)
│   ├── .env.example             # ✅ Template para Git
│   ├── .gitignore               # ✅ Configurado
│   ├── LICENSE                  # ✅ MIT License
│   ├── README.md                # ✅ Documentación completa
│   ├── requirements.txt         # Dependencias
│   └── *.md                     # Documentación adicional
│
├── logs/                        # Logs del servidor
├── error_docs/                  # Páginas de error
└── .composer/                   # Composer cache
```

## 📋 Checklist para Repositorio Git

- [x] README.md completo y detallado
- [x] .gitignore configurado
- [x] .env.example con template
- [x] LICENSE (MIT)
- [x] .gitkeep en carpetas de uploads
- [x] Documentación adicional (MULTIUSUARIO, PWA, SECURITY, STYLE_GUIDE)
- [ ] Eliminar archivos innecesarios antes de commit inicial
- [ ] Verificar que .env no se suba a Git
- [ ] Verificar que instance/shopqr.db no se suba a Git
- [ ] Verificar que uploads con imágenes no se suban a Git

## 🚀 Comandos para Preparar Repositorio

```bash
# Ir al directorio de producción
cd /var/www/vhosts/tag2qr.shop/httpdocs

# Inicializar Git (si no está inicializado)
git init

# Agregar remote
git remote add origin https://github.com/cdavidg/Tag2QR.git

# Verificar qué archivos se incluirán (revisar que .gitignore funcione)
git status

# Archivos que NO deben aparecer:
# - .env (debe estar ignorado)
# - instance/shopqr.db (debe estar ignorado)
# - uploads/products/* (excepto .gitkeep)
# - __pycache__/ (debe estar ignorado)
# - venv/ (debe estar ignorado)

# Agregar archivos al staging
git add .

# Commit inicial
git commit -m "Initial commit: Tag2QR v1.0 - Sistema de gestión de productos con QR dinámicos"

# Push al repositorio
git branch -M main
git push -u origin main
```

## 🔐 Verificación de Seguridad Pre-Commit

**IMPORTANTE:** Antes de hacer push, verificar que NO se suban:

```bash
# Verificar que estos archivos NO estén en staging
git status | grep -E "\.env$|shopqr\.db|uploads/products/[0-9]|uploads/qr/.*\.png"

# Si aparecen, agregarlos a .gitignore
echo "*.db" >> .gitignore
echo ".env" >> .gitignore
```

## 📝 Archivos a Excluir del Repositorio

### Sensibles (Seguridad)
- `.env` - Contiene SECRET_KEY y configuración sensible
- `instance/shopqr.db` - Base de datos con información real de usuarios

### Generados (No necesarios)
- `__pycache__/` - Bytecode de Python
- `*.pyc`, `*.pyo` - Archivos compilados
- `venv/` - Entorno virtual (cada dev crea el suyo)

### Contenido de Usuario (Privacidad)
- `uploads/products/*` - Imágenes subidas por usuarios
- `uploads/qr/*` - QR generados
- `uploads/store/*` - Logos de tiendas

### Temporales
- `tmp/` - Archivos temporales
- `*.log` - Logs
- `.well-known/` - Configuración de dominio

## 🎉 Resultado Final

Después de seguir estos pasos, tendrás:

1. ✅ Repositorio limpio en GitHub con código fuente
2. ✅ Documentación profesional y completa
3. ✅ Licencia open source (MIT)
4. ✅ Configuración de ejemplo sin datos sensibles
5. ✅ Estructura clara y organizada
6. ✅ Sin archivos sensibles expuestos
7. ✅ Listo para contribuciones de la comunidad

---

**Última actualización:** 27 de octubre de 2025
**Autor:** David García
**Repositorio:** https://github.com/cdavidg/Tag2QR
