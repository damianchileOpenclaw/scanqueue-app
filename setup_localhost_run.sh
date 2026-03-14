#!/bin/bash

# Script para crear enlaces públicos con localhost.run
# No requiere autenticación - Gratuito y sencillo

echo "🌐 Configurando enlaces públicos con localhost.run..."
echo "====================================================="

# Primero, iniciar el servidor ScanQueue
echo "🚀 Iniciando servidor ScanQueue..."

cd "$(dirname "$0")"

# Verificar virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creando virtual environment..."
    python3 -m venv venv
fi

# Activar virtual environment
source venv/bin/activate

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt --quiet > /dev/null 2>&1

# Inicializar base de datos
echo "🗄️ Inicializando base de datos..."
python3 -c "
from app import init_db, init_default_queues
init_db()
init_default_queues()
print('✅ Base de datos lista')
" 2>/dev/null || echo "⚠️  Base de datos ya existe"

# Detener servidor si ya está corriendo
pkill -f "python.*app.py" 2>/dev/null || true

# Iniciar servidor en puerto 5000
echo "🌐 Iniciando servidor en puerto 5000..."
python app.py > scanqueue.log 2>&1 &
SERVER_PID=$!

echo "⏳ Esperando que el servidor inicie..."
sleep 8

# Verificar si el servidor está corriendo
if ! curl -s http://localhost:5000/ > /dev/null; then
    echo "❌ No se pudo iniciar el servidor"
    echo "Revisa el archivo scanqueue.log para más detalles"
    exit 1
fi

echo "✅ Servidor ScanQueue iniciado correctamente (PID: $SERVER_PID)"

# Ahora crear tunnel con localhost.run
echo "🔗 Creando tunnel público con localhost.run..."
echo "⏳ Esto puede tomar unos segundos..."

# Usar ssh para crear tunnel
PUBLIC_URL=$(ssh -o StrictHostKeyChecking=no -R 80:localhost:5000 nokey@localhost.run 2>&1 | grep -o 'https://[^ ]*\.lhrt\.link' | head -1)

if [ -z "$PUBLIC_URL" ]; then
    # Intentar otro método
    PUBLIC_URL=$(ssh -o StrictHostKeyChecking=no -R 80:localhost:5000 nokey@localhost.run 2>&1 | grep -o 'https://[^ ]*' | grep localhost.run | head -1)
fi

if [ -z "$PUBLIC_URL" ]; then
    echo "❌ No se pudo crear tunnel con localhost.run"
    echo "Intentando método alternativo..."
    
    # Método alternativo con serveo
    PUBLIC_URL=$(ssh -o StrictHostKeyChecking=no -R 80:localhost:5000 serveo.net 2>&1 | grep -o 'https://[^ ]*\.serveo\.net' | head -1)
fi

if [ -z "$PUBLIC_URL" ]; then
    echo "❌ No se pudieron crear enlaces públicos automáticamente"
    echo ""
    echo "📋 SOLUCIONES ALTERNATIVAS:"
    echo "1. Usa ngrok con cuenta gratuita:"
    echo "   - Registrate en: https://ngrok.com"
    echo "   - Obtén tu token"
    echo "   - Ejecuta: ngrok config add-authtoken TU_TOKEN"
    echo "   - Luego: ./setup_public_links.sh"
    echo ""
    echo "2. Usa tu propia IP pública:"
    echo "   - Necesitas un servidor/VPS"
    echo "   - Ejecuta: ./deploy.sh"
    echo "   - Abre puerto 5000 en firewall"
    echo ""
    echo "3. Servicios cloud gratuitos:"
    echo "   - Railway.app"
    echo "   - Render.com"
    echo "   - Fly.io"
    echo ""
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

echo ""
echo "🎉 ¡ENLACES PÚBLICOS CREADOS! 🎉"
echo "=================================================="
echo ""
echo "🌍 **ENLACES PARA CLIENTES:**"
echo "   📱 Página de Clientes:  ${PUBLIC_URL}/customer"
echo "   🏠 Página Principal:    ${PUBLIC_URL}/"
echo ""
echo "👨‍💼 **ENLACES PARA ADMINISTRADORES:**"
echo "   🔧 Panel de Admin:      ${PUBLIC_URL}/admin"
echo ""
echo "📊 **ENLACES DE MONITOREO:**"
echo "   📈 Dashboard:           ${PUBLIC_URL}/"
echo "   🔌 Estado API:          ${PUBLIC_URL}/api/queues"
echo ""
echo "📱 **CÓDIGOS QR RECOMENDADOS:**"
echo "   • Genera QR para: ${PUBLIC_URL}/customer"
echo "   • Colócalo en la entrada de tu negocio"
echo ""
echo "🔧 **INFORMACIÓN TÉCNICA:"
echo "   • Servidor local: http://localhost:5000"
echo "   • PID Servidor:   $SERVER_PID"
echo "   • URL Pública:    $PUBLIC_URL"
echo "   • Logs servidor:  scanqueue.log"
echo ""
echo "🛑 **PARA DETENER EL SISTEMA:**"
echo "   Ejecuta: pkill -f 'python.*app.py'"
echo "   O usa: ./stop_public_links.sh"
echo ""
echo "⚠️  **IMPORTANTE:**"
echo "   • Estos enlaces son TEMPORALES"
echo "   • Se reinician cada 24 horas aprox."
echo "   • Para producción usa servidor dedicado"
echo ""
echo "🚀 **PARA GENERAR CÓDIGOS QR:**"
echo "   python generate_qr_codes.py '$PUBLIC_URL'"
echo ""
echo "=================================================="
echo "✅ Sistema listo para uso global 🌎"
echo ""

# Guardar URLs en archivo
cat > PUBLIC_LINKS_LOCALHOST.txt << EOF
ENLACES PÚBLICOS SCANQUEUE (localhost.run)
===========================================
Fecha: $(date)
URL Base: ${PUBLIC_URL}

ENLACES CLIENTES:
- Página principal: ${PUBLIC_URL}/
- Tomar número: ${PUBLIC_URL}/customer
- Ver estado: ${PUBLIC_URL}/customer (con número)

ENLACES ADMINISTRACIÓN:
- Panel admin: ${PUBLIC_URL}/admin
- API queues: ${PUBLIC_URL}/api/queues

INFORMACIÓN TÉCNICA:
- Servidor local: http://localhost:5000
- PID Servidor: $SERVER_PID

PARA DETENER:
Ejecutar: pkill -f 'python.*app.py'
O: ./stop_public_links.sh

PARA QR CODES:
python generate_qr_codes.py '${PUBLIC_URL}'
EOF

echo "📄 URLs guardadas en: PUBLIC_LINKS_LOCALHOST.txt"
echo ""
echo "🔄 Generando códigos QR automáticamente..."
python generate_qr_codes.py "$PUBLIC_URL"

echo ""
echo "✅ ¡Todo listo! Los enlaces son:"
echo "   👤 Clientes:    ${PUBLIC_URL}/customer"
echo "   👨‍💼 Admin:       ${PUBLIC_URL}/admin"
echo "   🏠 Inicio:       ${PUBLIC_URL}/"

# Mantener el script corriendo para mantener el tunnel
echo ""
echo "📡 Manteniendo tunnel activo..."
echo "   Presiona Ctrl+C para detener"
echo ""

# Mantener el proceso activo
wait $SERVER_PID