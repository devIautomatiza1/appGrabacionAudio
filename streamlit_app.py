#!/usr/bin/env python3
"""
streamlit_app.py - Entrada principal para Streamlit Cloud
Configura correctamente los paths y ejecuta frontend/index.py
"""
import sys
import os
from pathlib import Path

# Obtener ruta raíz
app_root = Path(__file__).parent

# Configurar paths ANTES de cualquier import
backend_path = str(app_root / "backend")
frontend_path = str(app_root / "frontend")

sys.path.insert(0, backend_path)
sys.path.insert(0, frontend_path)
sys.path.insert(0, str(app_root))

# Cambiar directorio de trabajo a la raíz
os.chdir(app_root)

# Ahora ejecutar el archivo principal del frontend
import runpy
index_path = str(app_root / "frontend" / "index.py")

# Ejecutar como si fuera el main
runpy.run_path(index_path, run_name="__main__")
