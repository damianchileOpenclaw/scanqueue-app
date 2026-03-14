#!/usr/bin/env python3
"""
Railway Helper - Herramienta para gestionar ScanQueue en Railway
"""

import sys
import os
import json
import subprocess
import argparse

def print_banner():
    banner = """
    ╔══════════════════════════════════════════════════════╗
    ║                RAILWAY HELPER v1.0                   ║
    ║      Herramienta para ScanQueue en Railway.app       ║
    ╚══════════════════════════════════════════════════════╝
    """
    print(banner)

def check_requirements():
    """Verifica que todas las dependencias estén instaladas"""
    print("🔍 Verificando dependencias...")
    
    requirements = [
        ("flask", "Flask"),
        ("flask_socketio", "Flask-SocketIO"),
        ("qrcode", "qrcode[pil]"),
    ]
    
    all_ok = True
    for module, name in requirements:
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} - Falta instalar")
            all_ok = False
    
    return all_ok

def generate_new_qr_codes(domain):
    """Genera nuevos QR codes para un dominio específico"""
    print(f"\n🎨 Generando QR codes para: {domain}")
    
    # Verificar que el dominio tenga https://
    if not domain.startswith("http"):
        domain = f"https://{domain}"
    
    # Crear directorio para QR codes
    qr_dir = "qr_codes_railway"
    os.makedirs(qr_dir, exist_ok=True)
    
    # URLs
    urls = {
        "cliente": f"{domain}/customer",
        "admin": f"{domain}/admin",
        "inicio": f"{domain}/",
    }
    
    try:
        import qrcode
        from PIL import Image, ImageDraw, ImageFont
        
        print("🔄 Creando códigos QR...")
        
        for name, url in urls.items():
            # Generar QR
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Añadir texto
            draw = ImageDraw.Draw(img)
            
            # Guardar
            filename = f"{qr_dir}/qr_{name}.png"
            img.save(filename)
            print(f"  ✅ QR {name}: {filename}")
        
        # Crear HTML para visualizar
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>ScanQueue QR Codes - Railway</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .container {{ max-width: 800px; margin: 0 auto; }}
                .qr-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }}
                .qr-item {{ text-align: center; padding: 15px; border: 1px solid #ddd; border-radius: 8px; }}
                h1 {{ color: #333; }}
                .url {{ font-size: 12px; color: #666; word-break: break-all; }}
                .domain {{ color: #007bff; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📱 ScanQueue QR Codes - Railway</h1>
                <p>Dominio: <span class="domain">{domain}</span></p>
                
                <div class="qr-grid">
                    <div class="qr-item">
                        <h3>👥 Para Clientes</h3>
                        <img src="qr_cliente.png" width="200" height="200">
                        <p class="url">{domain}/customer</p>
                        <p>Escanear para tomar número</p>
                    </div>
                    
                    <div class="qr-item">
                        <h3>👨‍💼 Para Administradores</h3>
                        <img src="qr_admin.png" width="200" height="200">
                        <p class="url">{domain}/admin</p>
                        <p>Panel de control</p>
                    </div>
                    
                    <div class="qr-item">
                        <h3>🏠 Página Principal</h3>
                        <img src="qr_inicio.png" width="200" height="200">
                        <p class="url">{domain}/</p>
                        <p>Monitor en tiempo real</p>
                    </div>
                </div>
                
                <div style="margin-top: 30px; padding: 15px; background: #f8f9fa; border-radius: 8px;">
                    <h3>📋 Instrucciones de uso:</h3>
                    <ol>
                        <li>Imprime los QR codes y colócalos en tu negocio</li>
                        <li>Los clientes escanean el QR "Para Clientes"</li>
                        <li>Tú usas el QR "Para Administradores" en tu teléfono/tablet</li>
                        <li>El monitor muestra la cola en tiempo real</li>
                    </ol>
                </div>
            </div>
        </body>
        </html>
        """
        
        html_file = f"{qr_dir}/visualizar_qr.html"
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"\n📄 HTML generado: {html_file}")
        print(f"📁 Todos los archivos en: {qr_dir}/")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generando QR codes: {e}")
        return False

def test_domain(domain):
    """Prueba si el dominio está accesible"""
    print(f"\n🔗 Probando dominio: {domain}")
    
    try:
        import requests
        
        # Asegurar https://
        if not domain.startswith("http"):
            test_url = f"https://{domain}/"
        else:
            test_url = f"{domain}/"
        
        print(f"  URL de prueba: {test_url}")
        
        try:
            response = requests.get(test_url, timeout=10)
            if response.status_code == 200:
                print(f"  ✅ Dominio accesible (HTTP {response.status_code})")
                return True
            else:
                print(f"  ⚠️ Dominio responde pero con código: {response.status_code}")
                return False
        except requests.exceptions.SSLError:
            # Intentar sin SSL
            test_url = test_url.replace("https://", "http://")
            try:
                response = requests.get(test_url, timeout=10)
                if response.status_code == 200:
                    print(f"  ✅ Dominio accesible (HTTP, sin SSL)")
                    return True
            except:
                pass
        
        print("  ❌ No se pudo acceder al dominio")
        return False
        
    except ImportError:
        print("  ⚠️ No se pudo importar requests. Instala: pip install requests")
        return None

def create_railway_config():
    """Crea archivo de configuración para Railway"""
    config = {
        "name": "scanqueue-app",
        "description": "ScanQueue - Sistema de colas en línea",
        "runtime": "python",
        "python_version": "3.12",
        "env": {
            "FLASK_ENV": "production",
            "PORT": "5000"
        },
        "scripts": {
            "start": "python app.py"
        }
    }
    
    with open("railway.config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ Archivo railway.config.json creado")

def main():
    parser = argparse.ArgumentParser(description="Railway Helper para ScanQueue")
    parser.add_argument("--domain", help="Tu dominio de Railway (ej: scanqueue-app-production.up.railway.app)")
    parser.add_argument("--test", action="store_true", help="Probar conexión al dominio")
    parser.add_argument("--qr", action="store_true", help="Generar nuevos QR codes")
    parser.add_argument("--config", action="store_true", help="Crear configuración para Railway")
    
    args = parser.parse_args()
    
    print_banner()
    
    if args.config:
        create_railway_config()
        return
    
    if not args.domain:
        print("❌ Debes especificar un dominio con --domain")
        print("\nEjemplo de uso:")
        print("  python railway_helper.py --domain scanqueue-app-production.up.railway.app --test --qr")
        print("  python railway_helper.py --domain https://tu-dominio.railway.app --qr")
        return
    
    if args.test:
        test_domain(args.domain)
    
    if args.qr:
        if check_requirements():
            generate_new_qr_codes(args.domain)
        else:
            print("\n⚠️ Instala las dependencias faltantes:")
            print("  pip install flask flask-socketio qrcode[pil] pillow")
    
    if not args.test and not args.qr:
        print("\n📋 Resumen de acciones disponibles:")
        print("  1. Probar dominio: --test")
        print("  2. Generar QR codes: --qr")
        print("  3. Crear configuración: --config")
        print("\n🎯 Ejemplo completo:")
        print("  python railway_helper.py --domain TU-DOMINIO --test --qr")

if __name__ == "__main__":
    main()