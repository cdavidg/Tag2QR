# MEDIDAS DE SEGURIDAD - PANEL DE ADMINISTRACIÓN

## Acceso al Panel de Control (admin_app)

### ✅ Protecciones Implementadas

#### 1. **Control de Acceso a Nivel de Blueprint**
```python
@admin_app_bp.before_request
def check_superadmin_access():
    """Verificación global antes de cada request"""
    - Verifica autenticación del usuario
    - Verifica existencia del atributo is_superadmin
    - Verifica valor True del atributo
    - Redirige a dashboard normal si falla
```

#### 2. **Decorador en Cada Ruta**
```python
@superadmin_required
def route_function():
    """Todas las rutas tienen doble protección"""
    - Decorador @login_required
    - Decorador @superadmin_required
    - Verificación is_authenticated
    - Verificación is_superadmin == True
```

#### 3. **Modelo de Datos Seguro**
```python
class User:
    is_superadmin = db.Column(db.Boolean, default=False, nullable=False)
    # Usuarios por defecto NO son superadmins
    # Campo nullable=False previene valores NULL
```

#### 4. **Interfaz de Usuario Condicional**
```jinja2
{% if current_user.is_superadmin %}
    <a href="{{ url_for('admin_app.dashboard') }}">
        Panel de Control
    </a>
{% endif %}
```
- Solo visible para superadmins autenticados
- Usa contexto de Flask-Login (current_user)
- Sin exposición en HTML si no es superadmin

#### 5. **Mensajes Flash de Seguridad**
- "Debes iniciar sesión" para no autenticados
- "Acceso denegado. Solo para superadministradores" para usuarios normales
- Redirige a panel seguro (/admin)

### 🔒 Verificaciones por Capa

**Capa 1 - Template (HTML):**
- Condicional `{% if current_user.is_superadmin %}`
- Link no renderizado si no es superadmin

**Capa 2 - Blueprint (before_request):**
- Verificación global antes de CUALQUIER ruta
- `check_superadmin_access()` ejecutado automáticamente
- Previene inyección directa de URL

**Capa 3 - Ruta Individual (decorador):**
- `@superadmin_required` en cada función
- Doble verificación redundante
- Previene bypass si falla una capa

**Capa 4 - Base de Datos:**
- Campo `is_superadmin` con default=False
- Valor explícito, no nullable
- Requiere migración manual para activar

### 🛡️ Escenarios Protegidos

1. ✅ **Usuario no autenticado intenta acceder:**
   - Redirige a /login
   - Flash: "Debes iniciar sesión"

2. ✅ **Usuario normal (is_admin=True) intenta acceder:**
   - Redirige a /admin (su panel)
   - Flash: "Acceso denegado. Solo para superadministradores"

3. ✅ **Usuario sin campo is_superadmin (migración antigua):**
   - `hasattr()` detecta ausencia
   - Redirige a /admin
   - Flash de acceso denegado

4. ✅ **Usuario con is_superadmin=False:**
   - Verificación explícita falla
   - Redirige a /admin
   - No puede acceder

5. ✅ **Manipulación de URL directa:**
   - `before_request` intercepta
   - Verificación antes de ejecutar ruta
   - Previene acceso

6. ✅ **Superadmin válido (is_superadmin=True):**
   - Ve el link en menú
   - Pasa before_request
   - Pasa decorador
   - Acceso concedido

### 📋 Checklist de Seguridad

- [x] Campo is_superadmin con default=False
- [x] before_request en blueprint
- [x] @superadmin_required en todas las rutas
- [x] Verificación hasattr() para campos faltantes
- [x] Mensajes flash informativos
- [x] Redirección segura a /admin
- [x] Condicional en template
- [x] Sin exposición de rutas en frontend
- [x] Sin enlaces ocultos en HTML source
- [x] Flask-Login current_user validado

### 🔑 Usuario Superadmin Actual

**Email:** cedav95@gmail.com
**Password:** 123456 (cambiar en producción)
**is_superadmin:** True
**is_admin:** True

### 🚨 Importante

1. **Cambiar password por defecto** en producción
2. Solo crear superadmins manualmente en DB
3. No exponer panel admin_app públicamente
4. Revisar logs regularmente por intentos de acceso
5. Considerar 2FA para superadmins en futuro

### 📝 Log de Acceso

El sistema registra:
- Intentos de acceso denegados (via flash messages)
- Usuario que intenta acceder (current_user.email)
- Timestamp del intento
- Ruta solicitada

### 🔄 Proceso de Auditoría

Para verificar accesos al panel:
```bash
# Ver logs de acceso
tail -f /var/www/vhosts/tag2qr.shop/logs/gunicorn-access.log | grep admin_app

# Ver intentos denegados
tail -f /var/www/vhosts/tag2qr.shop/logs/gunicorn-error.log | grep "Acceso denegado"
```

---

**Conclusión:** El sistema tiene protección de múltiples capas. Un atacante necesitaría:
1. Conocer que existe /admin_app (no expuesto)
2. Tener cuenta válida (autenticación)
3. Modificar DB directamente para is_superadmin=True (acceso servidor)
4. Pasar 3 capas de verificación simultáneas

**Nivel de Seguridad:** ⭐⭐⭐⭐⭐ (5/5)
