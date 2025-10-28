"""
Script para crear un usuario administrador
"""
import os
import sys
import importlib.util

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar el archivo app.py directamente (no el paquete app/)
spec = importlib.util.spec_from_file_location("app_module", os.path.join(os.path.dirname(__file__), "app.py"))
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)

from app.models import db, User

def create_admin():
    application = app_module.create_app()
    
    with application.app_context():
        # Crear tablas si no existen
        db.create_all()
        
        print("\n=== Crear Usuario Administrador ===\n")
        
        email = input("Email: ").strip()
        if not email:
            print("Error: El email es requerido")
            return
        
        # Verificar si el usuario ya existe
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f"\n⚠️  El usuario con email '{email}' ya existe.")
            reset = input("¿Desea resetear la contraseña? (s/n): ").lower()
            if reset == 's':
                password = input("Nueva contraseña: ").strip()
                if len(password) < 6:
                    print("Error: La contraseña debe tener al menos 6 caracteres")
                    return
                
                existing_user.set_password(password)
                db.session.commit()
                print(f"\n✅ Contraseña actualizada para {email}")
                print(f"\nPuedes iniciar sesión en: http://127.0.0.1:5000/admin/login")
                print(f"Email: {email}")
                print(f"Password: {password}\n")
            return
        
        password = input("Contraseña (mínimo 6 caracteres): ").strip()
        if len(password) < 6:
            print("Error: La contraseña debe tener al menos 6 caracteres")
            return
        
        # Crear usuario
        user = User(email=email, is_admin=True)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        print(f"\n✅ Usuario administrador creado exitosamente!")
        print(f"\nCredenciales:")
        print(f"Email: {email}")
        print(f"Password: {password}")
        print(f"\nPuedes iniciar sesión en: http://127.0.0.1:5000/admin/login\n")

if __name__ == '__main__':
    create_admin()