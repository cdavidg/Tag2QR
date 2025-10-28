#!/usr/bin/env python3
"""
Passenger WSGI file para Tag2QR
"""
import sys
import os

# Configurar intérprete de Python
INTERP = "/var/www/vhosts/tag2qr.shop/httpdocs/venv/bin/python3"
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Agregar directorio actual al path
sys.path.insert(0, '/var/www/vhosts/tag2qr.shop/httpdocs')

# Importar la aplicación
import importlib.util
spec = importlib.util.spec_from_file_location("app_module", "/var/www/vhosts/tag2qr.shop/httpdocs/app.py")
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)

# Exponer la aplicación para Passenger
application = app_module.app
