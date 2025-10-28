# GUÍA DE ESTILO - PANEL DE ADMINISTRACIÓN TAG2QR
## Reglas Generales para Todos los Módulos

### 🎨 TEMA Y COLORES

**Tema Oscuro - Solo Blanco y Negro:**
- Fondo principal: `#000000` (negro puro)
- Fondo secundario: `#0a0a0a` (negro suave)
- Cards/Contenedores: `#1a1a1a` (gris muy oscuro)
- Bordes: `#333333` (gris oscuro)
- Hover states: `#2a2a2a` (gris medio-oscuro)

**Texto:**
- Texto principal: `#ffffff` (blanco puro)
- Texto secundario: `#cccccc` (gris claro)
- Texto deshabilitado/labels: `#999999` (gris medio)
- Texto placeholder: `#666666` (gris)

**NO SE PERMITEN COLORES:** Solo se usa escala de grises (blanco y negro).

### 🔤 ICONOS

**Font Awesome 6.4.0:**
```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
```

**Iconos Principales:**
- Dashboard: `fas fa-chart-line`
- Usuarios: `fas fa-users`
- Productos: `fas fa-box`
- Tiendas: `fas fa-store`
- Estadísticas: `fas fa-chart-bar`
- Configuración: `fas fa-cog`
- Editar: `fas fa-edit`
- Eliminar: `fas fa-trash`
- Guardar: `fas fa-save`
- Ver: `fas fa-eye`
- Filtrar: `fas fa-filter`
- Buscar: `fas fa-search`
- Agregar: `fas fa-plus`
- Cerrar sesión: `fas fa-sign-out-alt`
- Usuario admin: `fas fa-user-shield`
- Super admin: `fas fa-crown`

### 📐 ESTRUCTURA HTML

**Cada página debe extender de base.html:**
```jinja2
{% extends "admin_app/base.html" %}

{% block title %}Título - Super Admin{% endblock %}
{% block page_icon %}fas fa-icon-name{% endblock %}
{% block page_title %}Título de la Página{% endblock %}

{% block content %}
<!-- Contenido aquí -->
{% endblock %}
```

### 🎯 COMPONENTES ESTÁNDAR

#### 1. CARDS
```html
<div class="card">
    <div class="card-header">
        <i class="fas fa-icon"></i> Título
    </div>
    <div class="card-body">
        <!-- Contenido -->
    </div>
</div>
```

#### 2. BOTONES
```html
<!-- Primario (Blanco sobre negro) -->
<button class="btn btn-primary">
    <i class="fas fa-icon"></i> Texto
</button>

<!-- Secundario (Transparente con borde) -->
<button class="btn btn-secondary">
    <i class="fas fa-icon"></i> Texto
</button>

<!-- Peligro (Negro con borde blanco) -->
<button class="btn btn-danger">
    <i class="fas fa-icon"></i> Texto
</button>

<!-- Éxito (Blanco sobre negro) -->
<button class="btn btn-success">
    <i class="fas fa-icon"></i> Texto
</button>
```

#### 3. TABLAS
```html
<table class="wp-list-table">
    <thead>
        <tr>
            <th>Columna 1</th>
            <th>Columna 2</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Dato 1</td>
            <td>Dato 2</td>
        </tr>
    </tbody>
</table>
```

#### 4. FORMULARIOS
```html
<form method="post">
    <div class="form-group">
        <label for="campo">
            <i class="fas fa-icon"></i> Label
        </label>
        <input type="text" 
               id="campo" 
               name="campo" 
               class="form-control" 
               placeholder="Texto">
        <small style="color: #999999;">Ayuda</small>
    </div>
    
    <button type="submit" class="btn btn-primary">
        <i class="fas fa-save"></i> Guardar
    </button>
</form>
```

#### 5. BADGES
```html
<!-- Éxito (blanco sobre negro) -->
<span class="badge badge-success">
    <i class="fas fa-check"></i> Texto
</span>

<!-- Peligro (negro con borde blanco) -->
<span class="badge badge-danger">
    <i class="fas fa-times"></i> Texto
</span>

<!-- Advertencia (gris) -->
<span class="badge badge-warning">Texto</span>

<!-- Info (gris claro) -->
<span class="badge badge-info">Texto</span>
```

#### 6. ALERTAS
```html
<!-- Éxito -->
<div class="alert alert-success">
    <i class="fas fa-check-circle"></i> Mensaje
</div>

<!-- Error -->
<div class="alert alert-danger">
    <i class="fas fa-exclamation-circle"></i> Mensaje
</div>

<!-- Advertencia -->
<div class="alert alert-warning">
    <i class="fas fa-exclamation-triangle"></i> Mensaje
</div>

<!-- Información -->
<div class="alert alert-info">
    <i class="fas fa-info-circle"></i> Mensaje
</div>
```

#### 7. WIDGETS DEL DASHBOARD
```html
<div class="dashboard-widgets">
    <div class="widget">
        <div class="widget-label">
            <i class="fas fa-icon"></i> Label
        </div>
        <div class="widget-value">123</div>
        <small style="color: #999999;">Descripción</small>
    </div>
</div>
```

#### 8. PAGINACIÓN
```html
<div class="pagination">
    <a href="#">« Anterior</a>
    <span class="active">1</span>
    <a href="#">2</a>
    <a href="#">3</a>
    <a href="#">Siguiente »</a>
</div>
```

### 📱 RESPONSIVE

- Sidebar colapsa a 60px en móviles
- Al hover se expande a 200px
- Grids usan `grid-template-columns: repeat(auto-fit, minmax(250px, 1fr))`
- Breakpoint principal: `@media (max-width: 768px)`

### ✅ CHECKLIST PARA NUEVOS MÓDULOS

- [ ] Extender de `admin_app/base.html`
- [ ] Definir `page_icon` con Font Awesome
- [ ] Usar solo colores blanco/negro/grises
- [ ] Agregar iconos Font Awesome a todos los elementos
- [ ] Cards con header e iconos
- [ ] Botones con iconos y clases estándar
- [ ] Tablas con clase `wp-list-table`
- [ ] Formularios con estructura `form-group`
- [ ] Badges con iconos cuando sea apropiado
- [ ] Responsive design aplicado
- [ ] Textos consistentes con guía de colores

### 🔒 SEGURIDAD

Todos los módulos deben usar el decorador:
```python
@superadmin_required
def mi_funcion():
    # código
```

### 📝 NOMENCLATURA

**Rutas:**
- `/admin_app/` - Dashboard principal
- `/admin_app/modulo_list` - Listado
- `/admin_app/modulo/<id>` - Detalle
- `/admin_app/modulo/<id>/edit` - Editar
- `/admin_app/modulo/<id>/delete` - Eliminar (POST)

**Templates:**
- `admin_app/modulo_list.html`
- `admin_app/modulo_detail.html`
- `admin_app/modulo_edit.html`

**Funciones:**
- `modulo_list()`
- `modulo_detail(id)`
- `modulo_edit(id)`
- `modulo_delete(id)`

---

## 🚀 EJEMPLO COMPLETO DE NUEVO MÓDULO

Ver archivos existentes en `templates/admin_app/` como referencia:
- `dashboard.html` - Widgets y estadísticas
- `user_list.html` - Listado con filtros
- `user_detail.html` - Vista detallada
- `user_edit.html` - Formulario de edición

**Mantén la consistencia visual en todos los módulos!**
