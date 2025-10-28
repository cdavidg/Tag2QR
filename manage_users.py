"""
Script simple para gestionar usuarios admin
Ejecutar con: python manage_users.py
"""
import os
import sys
from getpass import getpass

# Configurar el path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Establecer variable de entorno antes de importar
os.environ['SECRET_KEY'] = 'dev-secret-key-for-admin-script'

def main():
    # Importar desde el archivo app.py (no el paquete app/)
    import importlib.util
    spec = importlib.util.spec_from_file_location("app_module", "app.py")
    app_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_module)
    
    from app.models import db, User
    
    flask_app = app_module.app
    
    with flask_app.app_context():
        # Crear tablas si no existen
        db.create_all()
        
        print("\n" + "="*50)
        print("   GESTIÓN DE USUARIOS ADMINISTRADORES")
        print("="*50 + "\n")
        
        # Mostrar usuarios existentes
        users = User.query.all()
        if users:
            print("📋 Usuarios existentes:")
            for i, user in enumerate(users, 1):
                print(f"  {i}. {user.email} (Creado: {user.created_at.strftime('%d/%m/%Y')})")
            print()
        else:
            print("⚠️  No hay usuarios registrados\n")
        
        print("Opciones:")
        print("1. Crear nuevo usuario")
        print("2. Resetear contraseña de usuario existente")
        print("3. Salir")
        
        opcion = input("\nSelecciona una opción (1-3): ").strip()
        
        if opcion == "1":
            crear_usuario()
        elif opcion == "2":
            resetear_password()
        elif opcion == "3":
            print("Adiós!")
            return
        else:
            print("Opción inválida")

def crear_usuario():
    import importlib.util
    spec = importlib.util.spec_from_file_location("app_module", "app.py")
    app_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_module)
    
    from app.models import db, User
    flask_app = app_module.app
    
    with flask_app.app_context():
        print("\n--- CREAR NUEVO USUARIO ---\n")
        
        email = input("Email: ").strip()
        if not email:
            print("❌ El email es requerido")
            return
        
        # Verificar si ya existe
        if User.query.filter_by(email=email).first():
            print(f"❌ Ya existe un usuario con el email '{email}'")
            return
        
        password = getpass("Contraseña (mínimo 6 caracteres): ").strip()
        if len(password) < 6:
            print("❌ La contraseña debe tener al menos 6 caracteres")
            return
        
        # Crear usuario
        user = User(email=email, is_admin=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        print(f"\n✅ Usuario creado exitosamente!")
        print(f"\n📝 Credenciales:")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
        print(f"\n🌐 Login: http://127.0.0.1:5000/admin/login\n")

def resetear_password():
    import importlib.util
    spec = importlib.util.spec_from_file_location("app_module", "app.py")
    app_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_module)
    
    from app.models import db, User
    flask_app = app_module.app
    
    with flask_app.app_context():
        print("\n--- RESETEAR CONTRASEÑA ---\n")
        
        users = User.query.all()
        if not users:
            print("❌ No hay usuarios registrados")
            return
        
        # Mostrar usuarios
        print("Usuarios disponibles:")
        for i, user in enumerate(users, 1):
            print(f"  {i}. {user.email}")
        
        try:
            seleccion = int(input("\nSelecciona el número de usuario: ").strip())
            if seleccion < 1 or seleccion > len(users):
                print("❌ Selección inválida")
                return
            
            user = users[seleccion - 1]
            password = getpass("Nueva contraseña (mínimo 6 caracteres): ").strip()
            
            if len(password) < 6:
                print("❌ La contraseña debe tener al menos 6 caracteres")
                return
            
            user.set_password(password)
            db.session.commit()
            
            print(f"\n✅ Contraseña actualizada!")
            print(f"\n📝 Nuevas credenciales:")
            print(f"   Email: {user.email}")
            print(f"   Password: {password}")
            print(f"\n🌐 Login: http://127.0.0.1:5000/admin/login\n")
            
        except ValueError:
            print("❌ Debes ingresar un número")
            return

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperación cancelada")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()