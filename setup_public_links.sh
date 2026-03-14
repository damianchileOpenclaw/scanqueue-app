#!/bin/bash

# Script para crear enlaces públicos con ngrok
# ScanQueue - Acceso global

echo "🌐 Configurando enlaces públicos para ScanQueue..."
echo "=================================================="

# Verificar si ngrok está instalado
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok no está instalado"
    echo "Instalando ngrok..."
    
    # Instalar ngrok
    curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
    sudo apt update
    sudo apt install -y ngrok
    
    if ! command -v ngrok &> /dev/null; then
        echo "⚠️  No se pudo instalar ngrok automáticamente"
        echo "Por favor instala ngrok manualmente:"
        echo "1. Visita: https://ngrok.com/download"
        echo "2. Sigue las instrucciones para tu sistema"
        echo "3. Configura tu token: ngrok config add-authtoken TU_TOKEN"
        exit 1
    fi
fi

# Verificar configuración de ngrok
if [ ! -f ~/.config/ngrok/ngrok.yml ]; then
    echo "⚠️  ngrok no está configurado"
    echo ""
    echo "📋 Para configurar ngrok necesitas:"
    echo "1. Crear cuenta en: https://ngrok.com"
    echo "2. Obtener tu token de autenticación"
    echo "3. Ejecutar: ngrok config add-authtoken TU_TOKEN"
    echo ""
    echo "🎯 Token gratuito:"
    echo "   - 1 tunnel simultáneo"
    echo "   - Conexiones limitadas"
    echo "   - Ideal para pruebas"
    echo ""
    echo "💳 Token premium (recomendado):"
    echo "   - Múltiples tunnels"
    echo "   - Dominios personalizados"
    echo "   - Sin límites de conexión"
    echo ""
    read -p "¿Tienes token de ngrok? (s/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        read -p "Ingresa tu token de ngrok: " NGROK_TOKEN
        ngrok config add-authtoken $NGROK_TOKEN
    else
        echo "🎁 Usando ngrok sin autenticación (limitado)"
    fi
fi

# Iniciar servidor ScanQueue en segundo plano
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
pip install -r requirements.txt --quiet

# Inicializar base de datos
echo "🗄️ Inicializando base de datos..."
python3 -c "
from app import init_db, init_default_queues
init_db()
init_default_queues()
print('✅ Base de datos lista')
"

# Detener servidor si ya está corriendo
pkill -f "python.*app.py" 2>/dev/null || true

# Iniciar servidor en puerto 5000
echo "🌐 Iniciando servidor en puerto 5000..."
python app.py > scanqueue.log 2>&1 &
SERVER_PID=$!

echo "⏳ Esperando que el servidor inicie..."
sleep 5

# Verificar si el servidor está corriendo
if ! curl -s http://localhost:5000/ > /dev/null; then
    echo "❌ No se pudo iniciar el servidor"
    echo "Revisa el archivo scanqueue.log para más detalles"
    exit 1
fi

echo "✅ Servidor ScanQueue iniciado correctamente (PID: $SERVER_PID)"

# Iniciar ngrok
echo "🔗 Iniciando ngrok para crear enlaces públicos..."
ngrok http 5000 > ngrok.log 2>&1 &
NGROK_PID=$!

echo "⏳ Esperando que ngrok se conecte..."
sleep 8

# Obtener URL de ngrok
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o 'https://[^"]*\.ngrok-free\.app')

if [ -z "$NGROK_URL" ]; then
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o 'https://[^"]*\.ngrok\.io')
fi

if [ -z "$NGROK_URL" ]; then
    echo "❌ No se pudo obtener URL de ngrok"
    echo "Revisa ngrok.log para más detalles"
    kill $SERVER_PID 2>/dev/null
    kill $NGROK_PID 2>/dev/null
    exit 1
fi

echo ""
echo "🎉 ¡ENLACES PÚBLICOS CREADOS! 🎉"
echo "=================================================="
echo ""
echo "🌍 **ENLACES PARA CLIENTES:**"
echo "   📱 Página de Clientes:  ${NGROK_URL}/customer"
echo "   🏠 Página Principal:    ${NGROK_URL}/"
echo ""
echo "👨‍💼 **ENLACES PARA ADMINISTRADORES:**"
echo "   🔧 Panel de Admin:      ${NGROK_URL}/admin"
echo ""
echo "📊 **ENLACES DE MONITOREO:**"
echo "   📈 Dashboard:           ${NGROK_URL}/"
echo "   🔌 Estado API:          ${NGROK_URL}/api/queues"
echo ""
echo "📱 **CÓDIGOS QR RECOMENDADOS:**"
echo "   • Genera QR para: ${NGROK_URL}/customer"
echo "   • Colócalo en la entrada de tu negocio"
echo ""
echo "🔧 **INFORMACIÓN TÉCNICA:"
echo "   • Servidor local: http://localhost:5000"
echo "   • PID Servidor:   $SERVER_PID"
echo "   • PID Ngrok:      $NGROK_PID"
echo "   • Logs servidor:  scanqueue.log"
echo "   • Logs ngrok:     ngrok.log"
echo ""
echo "🛑 **PARA DETENER EL SISTEMA:**"
echo "   Ejecuta: ./stop_public_links.sh"
echo ""
echo "⚠️  **IMPORTANTE:**"
echo "   • Estos enlaces son TEMPORALES (duración variable)"
echo "   • Ngrok free tiene límites de conexión"
echo "   • Para producción, recomiendo servidor con IP fija"
echo ""
echo "📝 **PARA ENLACES PERMANENTES:**"
echo "   1. Contrata VPS (DigitalOcean, AWS, etc.)"
echo "   2. Usa el script deploy.sh"
echo "   3. Configura dominio personalizado"
echo ""
echo "=================================================="
echo "✅ Sistema listo para uso global 🌎"
echo ""

# Guardar URLs en archivo
cat > PUBLIC_LINKS.txt << EOF
ENLACES PÚBLICOS SCANQUEUE
==========================
Fecha: $(date)
URL Base: ${NGROK_URL}

ENLACES CLIENTES:
- Página principal: ${NGROK_URL}/
- Tomar número: ${NGROK_URL}/customer
- Ver estado: ${NGROK_URL}/customer (con número)

ENLACES ADMINISTRACIÓN:
- Panel admin: ${NGROK_URL}/admin
- API queues: ${NGROK_URL}/api/queues

INFORMACIÓN TÉCNICA:
- Servidor local: http://localhost:5000
- PID Servidor: $SERVER_PID
- PID Ngrok: $NGROK_PID

PARA DETENER:
Ejecutar: ./stop_public_links.sh
EOF

echo "📄 URLs guardadas en: PUBLIC_LINKS.txt"
echo "🔗 También puedes escanear este código QR:"