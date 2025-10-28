#!/usr/bin/env python3
"""
Script para agregar campo is_superadmin al modelo User y crear superadmin
"""
import os
import sys

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(__file__))

if __name__ == '__main__':
    # Importar la función create_app
    import importlib.util
    spec = importlib.util.spec_from_file_location("app_main", "app.py")
    app_main = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_main)
    
    from app.models import db, User
    from sqlalchemy import text
    
    app = app_main.create_app()
    
    with app.app_context():
        try:
            # 1. Agregar columna is_superadmin si no existe
            print("Verificando estructura de la base de datos...")
            
            with db.engine.connect() as conn:
                # Verificar si la columna ya existe
                result = conn.execute(text("PRAGMA table_info(user)"))
                columns = [row[1] for row in result]
                
                if 'is_superadmin' not in columns:
                    print("Agregando columna is_superadmin...")
                    conn.execute(text("ALTER TABLE user ADD COLUMN is_superadmin BOOLEAN DEFAULT 0 NOT NULL"))
                    conn.commit()
                    print("✓ Columna is_superadmin agregada")
                else:
                    print("✓ Columna is_superadmin ya existe")
            
            # 2. Buscar o crear usuario superadmin
            print("\nConfigurando superadmin...")
            superadmin = User.query.filter_by(email='cedav95@gmail.com').first()
            
            if superadmin:
                print(f"Usuario encontrado: {superadmin.email}")
                superadmin.is_superadmin = True
                superadmin.is_admin = True
                # No cambiar contraseña si ya existe
                print("✓ Usuario marcado como superadmin")
            else:
                print("Creando nuevo usuario superadmin...")
                superadmin = User(
                    email='cedav95@gmail.com',
                    is_admin=True,
                    is_superadmin=True
                )
                superadmin.set_password('123456')
                db.session.add(superadmin)
                print("✓ Usuario superadmin creado")
            
            db.session.commit()
            
            # 3. Verificar
            print("\nVerificación:")
            all_superadmins = User.query.filter_by(is_superadmin=True).all()
            print(f"Superadministradores en el sistema: {len(all_superadmins)}")
            for sa in all_superadmins:
                print(f"  - {sa.email} (ID: {sa.id})")
            
            print("\n✓ Migración completada exitosamente")
            print("\nCredenciales de acceso:")
            print("  Email: cedav95@gmail.com")
            print("  Password: 123456")
            print("  URL: https://tag2qr.shop/admin_app")
            
        except Exception as e:
            print(f"\n✗ Error durante la migración: {e}")
            db.session.rollback()
            import traceback
            traceback.print_exc()
            sys.exit(1)
