#!/usr/bin/env python3
"""
Generador de códigos QR para ScanQueue
"""

import qrcode
import os
from PIL import Image, ImageDraw, ImageFont
import sys

def generate_qr_code(url, filename, title="ScanQueue"):
    """Genera un código QR con diseño personalizado"""
    
    # Crear código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Crear imagen QR
    qr_img = qr.make_image(fill_color="#667eea", back_color="white")
    
    # Crear imagen con título
    width, height = qr_img.size
    new_height = height + 80  # Espacio para el título
    
    # Crear nueva imagen
    new_img = Image.new('RGB', (width, new_height), 'white')
    new_img.paste(qr_img, (0, 60))
    
    # Añadir título
    draw = ImageDraw.Draw(new_img)
    
    # Intentar usar una fuente, si no está disponible usar default
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    # Dibujar título
    title_width = draw.textlength(title, font=font)
    draw.text(((width - title_width) // 2, 20), title, fill="#333333", font=font)
    
    # Dibujar URL (recortada si es muy larga)
    url_display = url.replace("https://", "").replace("http://", "")
    if len(url_display) > 30:
        url_display = url_display[:27] + "..."
    
    url_width = draw.textlength(url_display, font=font)
    draw.text(((width - url_width) // 2, new_height - 30), url_display, fill="#666666", font=font)
    
    # Guardar imagen
    new_img.save(filename)
    print(f"✅ QR generado: {filename}")
    
    return new_img

def main():
    """Función principal"""
    
    print("🎨 Generador de códigos QR para ScanQueue")
    print("=========================================")
    
    # Pedir URL base
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = input("Ingresa la URL base (ej: https://xxxx.ngrok-free.app): ").strip()
    
    if not base_url:
        print("❌ Se necesita una URL")
        return
    
    # Crear directorio para QR codes
    qr_dir = "qr_codes"
    os.makedirs(qr_dir, exist_ok=True)
    
    # URLs para generar
    urls = {
        "cliente": f"{base_url}/customer",
        "admin": f"{base_url}/admin",
        "inicio": base_url
    }
    
    print(f"\n🌐 URL Base: {base_url}")
    print(f"📁 Guardando QR codes en: {qr_dir}/")
    print("\n🔄 Generando códigos QR...")
    
    # Generar QR codes
    for name, url in urls.items():
        filename = f"{qr_dir}/qr_{name}.png"
        title = f"ScanQueue - {name.capitalize()}"
        generate_qr_code(url, filename, title)
    
    # Crear imagen combinada (opcional)
    try:
        print("\n🖼️  Creando imagen combinada...")
        
        # Cargar las 3 imágenes
        images = []
        for name in ["cliente", "admin", "inicio"]:
            img_path = f"{qr_dir}/qr_{name}.png"
            if os.path.exists(img_path):
                images.append(Image.open(img_path))
        
        if len(images) == 3:
            # Calcular dimensiones
            widths, heights = zip(*(i.size for i in images))
            total_width = sum(widths)
            max_height = max(heights)
            
            # Crear nueva imagen
            combined = Image.new('RGB', (total_width, max_height), 'white')
            
            # Pegar imágenes
            x_offset = 0
            for img in images:
                combined.paste(img, (x_offset, 0))
                x_offset += img.size[0]
            
            # Guardar imagen combinada
            combined.save(f"{qr_dir}/qr_combinado.png")
            print(f"✅ QR combinado generado: {qr_dir}/qr_combinado.png")
    except Exception as e:
        print(f"⚠️  No se pudo crear imagen combinada: {e}")
    
    # Crear archivo HTML para visualización
    html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Códigos QR - ScanQueue</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
        }}
        .qr-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
        }}
        .qr-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            text-align: center;
            flex: 1;
            min-width: 250px;
        }}
        .qr-card img {{
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 5px;
        }}
        .url {{
            margin-top: 10px;
            font-size: 0.9rem;
            color: #666;
            word-break: break-all;
        }}
        .instructions {{
            margin-top: 30px;
            padding: 20px;
            background: #fff3cd;
            border-radius: 10px;
            border-left: 5px solid #ffc107;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📱 Códigos QR - ScanQueue</h1>
        <p>URL Base: {base_url}</p>
    </div>
    
    <div class="qr-container">
        <div class="qr-card">
            <h3>👤 Para Clientes</h3>
            <img src="qr_cliente.png" alt="QR Clientes">
            <div class="url">{urls['cliente']}</div>
            <p><strong>Uso:</strong> Escanear para tomar número</p>
        </div>
        
        <div class="qr-card">
            <h3>👨‍💼 Para Administradores</h3>
            <img src="qr_admin.png" alt="QR Admin">
            <div class="url">{urls['admin']}</div>
            <p><strong>Uso:</strong> Acceso al panel de control</p>
        </div>
        
        <div class="qr-card">
            <h3>🏠 Página Principal</h3>
            <img src="qr_inicio.png" alt="QR Inicio">
            <div class="url">{urls['inicio']}</div>
            <p><strong>Uso:</strong> Información general</p>
        </div>
    </div>
    
    <div class="instructions">
        <h3>📋 Instrucciones de Uso:</h3>
        <ol>
            <li><strong>Imprime</strong> los códigos QR en tamaño adecuado</li>
            <li><strong>Coloca</strong> el QR de clientes en la entrada</li>
            <li><strong>Comparte</strong> el QR de admin con tu personal</li>
            <li><strong>Verifica</strong> que los enlaces funcionen antes de imprimir</li>
            <li><strong>Actualiza</strong> los QR si cambia la URL</li>
        </ol>
        <p><strong>💡 Consejo:</strong> Usa papel resistente y lamina los códigos QR para mayor durabilidad.</p>
    </div>
</body>
</html>
"""
    
    with open(f"{qr_dir}/visualizar_qr.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"\n📄 HTML generado: {qr_dir}/visualizar_qr.html")
    print("\n🎉 ¡Códigos QR generados exitosamente!")
    print("\n📋 Resumen:")
    print(f"   • QR Clientes:    {qr_dir}/qr_cliente.png")
    print(f"   • QR Admin:       {qr_dir}/qr_admin.png")
    print(f"   • QR Inicio:      {qr_dir}/qr_inicio.png")
    print(f"   • QR Combinado:   {qr_dir}/qr_combinado.png")
    print(f"   • Visualizador:   {qr_dir}/visualizar_qr.html")
    print("\n🚀 Para usar: Imprime los QR y colócalos en lugares visibles")

if __name__ == "__main__":
    main()