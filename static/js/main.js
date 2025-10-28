// JavaScript básico para funcionalidades adicionales

// ==========================================
// PWA - Registro del Service Worker
// ==========================================
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // Verificar si es HTTPS o localhost
        const isSecureContext = window.isSecureContext;
        const isLocalhost = window.location.hostname === 'localhost' || 
                           window.location.hostname === '127.0.0.1' ||
                           window.location.hostname === '[::1]';
        
        if (!isSecureContext && !isLocalhost) {
            console.warn('⚠️ PWA requiere HTTPS para funcionar en producción');
            showHttpsWarning();
            return;
        }
        
        navigator.serviceWorker.register('/static/service-worker.js')
            .then((registration) => {
                console.log('✅ Service Worker registrado:', registration.scope);
                
                // Verificar actualizaciones periódicamente
                setInterval(() => {
                    registration.update();
                }, 60000); // Cada minuto
                
                // Manejar actualizaciones del service worker
                registration.addEventListener('updatefound', () => {
                    const newWorker = registration.installing;
                    
                    newWorker.addEventListener('statechange', () => {
                        if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                            // Hay una nueva versión disponible
                            if (confirm('Nueva versión disponible. ¿Actualizar ahora?')) {
                                newWorker.postMessage({ type: 'SKIP_WAITING' });
                                window.location.reload();
                            }
                        }
                    });
                });
            })
            .catch((error) => {
                console.error('❌ Error al registrar Service Worker:', error);
                showHttpsWarning();
            });
        
        // Recargar cuando el service worker toma control
        let refreshing = false;
        navigator.serviceWorker.addEventListener('controllerchange', () => {
            if (!refreshing) {
                refreshing = true;
                window.location.reload();
            }
        });
    });
}

function showHttpsWarning() {
    console.warn('⚠️ PWA requiere HTTPS. Usa ngrok o localtunnel para probar en móvil.');
    
    // Solo mostrar en móvil
    if (!/Android|iPhone|iPad|iPod/i.test(navigator.userAgent)) {
        return;
    }
    
    const warning = document.createElement('div');
    warning.innerHTML = `
        <div style="
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: #ff9800;
            color: white;
            padding: 12px 16px;
            text-align: center;
            z-index: 99999;
            font-size: 14px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        ">
            <strong>⚠️ Se requiere HTTPS</strong><br>
            <small>Para instalar la app en móvil necesitas acceso por HTTPS</small>
        </div>
    `;
    document.body.appendChild(warning);
}

// ==========================================
// PWA - Prompt de instalación
// ==========================================
let deferredPrompt;
const installButton = document.getElementById('install-pwa-button');

window.addEventListener('beforeinstallprompt', (e) => {
    console.log('💡 PWA puede ser instalada');
    
    // Prevenir el prompt automático
    e.preventDefault();
    deferredPrompt = e;
    
    // Solo mostrar banner de instalación si estamos en el área de admin
    if (window.location.pathname.startsWith('/admin')) {
        showInstallBanner();
    } else {
        console.log('⚠️ PWA solo se puede instalar desde el área de administración');
    }
});

function showInstallBanner() {
    // Verificar si ya está instalada o si el usuario la rechazó antes
    if (window.matchMedia('(display-mode: standalone)').matches) {
        console.log('✅ PWA ya está instalada');
        return;
    }
    
    if (localStorage.getItem('pwa-install-dismissed') === 'true') {
        return;
    }
    
    // Crear banner de instalación
    const banner = document.createElement('div');
    banner.id = 'pwa-install-banner';
    banner.innerHTML = `
        <div style="
            position: fixed;
            bottom: 16px;
            left: 16px;
            right: 16px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 16px;
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
            z-index: 10000;
            animation: slideUp 0.3s ease-out;
            max-width: 500px;
            margin: 0 auto;
        ">
            <div style="display: flex; align-items: flex-start; gap: 16px;">
                <div style="
                    background: rgba(255, 255, 255, 0.2);
                    border-radius: 12px;
                    width: 56px;
                    height: 56px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    flex-shrink: 0;
                ">
                    <i class="fas fa-mobile-screen-button" style="font-size: 28px;"></i>
                </div>
                <div style="flex: 1; min-width: 0;">
                    <h4 style="
                        margin: 0 0 6px 0;
                        font-size: 18px;
                        font-weight: 700;
                        letter-spacing: -0.02em;
                    ">Instalar Tag2QR</h4>
                    <p style="
                        margin: 0 0 16px 0;
                        font-size: 14px;
                        opacity: 0.95;
                        line-height: 1.4;
                    ">Agrega la app a tu pantalla de inicio para acceso rápido y sin conexión</p>
                    <div style="display: flex; gap: 12px;">
                        <button onclick="installPWA()" style="
                            background: white;
                            color: #667eea;
                            border: none;
                            padding: 12px 24px;
                            border-radius: 10px;
                            cursor: pointer;
                            font-weight: 700;
                            font-size: 14px;
                            flex: 1;
                            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                            transition: transform 0.2s, box-shadow 0.2s;
                        " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.15)'" 
                           onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 8px rgba(0,0,0,0.1)'">
                            <i class="fas fa-download" style="margin-right: 6px;"></i>Instalar
                        </button>
                        <button onclick="dismissInstallBanner()" style="
                            background: rgba(255, 255, 255, 0.15);
                            color: white;
                            border: none;
                            padding: 12px 20px;
                            border-radius: 10px;
                            cursor: pointer;
                            font-weight: 600;
                            font-size: 14px;
                            transition: background 0.2s;
                        " onmouseover="this.style.background='rgba(255,255,255,0.25)'" 
                           onmouseout="this.style.background='rgba(255,255,255,0.15)'">
                            Ahora no
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Agregar animación CSS
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    `;
    document.head.appendChild(style);
    
    document.body.appendChild(banner);
}

window.installPWA = async function() {
    const banner = document.getElementById('pwa-install-banner');
    
    if (!deferredPrompt) {
        console.log('❌ No hay prompt de instalación disponible');
        return;
    }
    
    // Mostrar el prompt
    deferredPrompt.prompt();
    
    // Esperar la respuesta del usuario
    const { outcome } = await deferredPrompt.userChoice;
    console.log(`Usuario ${outcome === 'accepted' ? 'aceptó' : 'rechazó'} la instalación`);
    
    if (outcome === 'accepted') {
        console.log('✅ PWA instalada exitosamente');
    } else {
        localStorage.setItem('pwa-install-dismissed', 'true');
    }
    
    // Limpiar
    deferredPrompt = null;
    if (banner) {
        banner.remove();
    }
};

window.dismissInstallBanner = function() {
    const banner = document.getElementById('pwa-install-banner');
    if (banner) {
        banner.remove();
    }
    localStorage.setItem('pwa-install-dismissed', 'true');
};

// Detectar cuando la app se instala
window.addEventListener('appinstalled', () => {
    console.log('✅ PWA instalada exitosamente');
    localStorage.removeItem('pwa-install-dismissed');
    
    // Ocultar banner si existe
    const banner = document.getElementById('pwa-install-banner');
    if (banner) {
        banner.remove();
    }
});

// Detectar si la app está corriendo como PWA instalada
if (window.matchMedia('(display-mode: standalone)').matches) {
    console.log('✅ Corriendo como PWA instalada');
    document.body.classList.add('pwa-installed');
}

// ==========================================
// Funcionalidades existentes
// ==========================================
document.addEventListener('DOMContentLoaded', function() {
    // Auto-generar SKU si está vacío
    const nameInput = document.querySelector('input[name="name"]');
    const skuInput = document.querySelector('input[name="sku"]');
    
    if (nameInput && skuInput) {
        nameInput.addEventListener('input', function() {
            if (!skuInput.value || skuInput.dataset.autogenerated === 'true') {
                const sku = generateSKU(this.value);
                skuInput.value = sku;
                skuInput.dataset.autogenerated = 'true';
            }
        });
        
        skuInput.addEventListener('input', function() {
            if (this.value) {
                this.dataset.autogenerated = 'false';
            }
        });
    }
    
    // Preview de imágenes
    const imageInput = document.querySelector('input[type="file"][name="images"]');
    if (imageInput) {
        imageInput.addEventListener('change', function(e) {
            previewImages(e.target.files);
        });
    }
});

function generateSKU(name) {
    if (!name) return '';
    
    // Limpiar el nombre y crear SKU
    const cleaned = name
        .toUpperCase()
        .replace(/[^A-Z0-9\s]/g, '')
        .replace(/\s+/g, '')
        .substring(0, 3);
    
    // Agregar números aleatorios
    const random = Math.floor(Math.random() * 1000).toString().padStart(3, '0');
    
    return `${cleaned || 'PRD'}${random}`;
}

function previewImages(files) {
    const existingPreview = document.querySelector('.image-preview');
    if (existingPreview) {
        existingPreview.remove();
    }
    
    if (files.length === 0) return;
    
    const preview = document.createElement('div');
    preview.className = 'image-preview';
    preview.innerHTML = '<h4>Vista previa de nuevas imágenes:</h4><div class="preview-grid"></div>';
    
    const grid = preview.querySelector('.preview-grid');
    grid.style.cssText = 'display: grid; grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); gap: 8px; margin-top: 8px;';
    
    Array.from(files).forEach(file => {
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.style.cssText = 'width: 100%; height: 120px; object-fit: cover; border: 1px solid #eee;';
                grid.appendChild(img);
            };
            reader.readAsDataURL(file);
        }
    });
    
    const imagesSection = document.querySelector('.form-section:has(input[name="images"])') || 
                         document.querySelector('input[name="images"]').closest('.form-section');
    if (imagesSection) {
        imagesSection.appendChild(preview);
    }
}

// Función para confirmar eliminación
function confirmDelete(message) {
    return confirm(message || '¿Estás seguro de que quieres eliminar este elemento?');
}

// Función para copiar al portapapeles
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showMessage('Copiado al portapapeles');
        });
    } else {
        // Fallback para navegadores más antiguos
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showMessage('Copiado al portapapeles');
    }
}

function showMessage(message, type = 'info') {
    const existing = document.querySelector('.js-message');
    if (existing) {
        existing.remove();
    }
    
    const messageEl = document.createElement('div');
    messageEl.className = `flash-message flash-${type} js-message`;
    messageEl.textContent = message;
    messageEl.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 1000; max-width: 300px;';
    
    document.body.appendChild(messageEl);
    
    setTimeout(() => {
        messageEl.remove();
    }, 3000);
}