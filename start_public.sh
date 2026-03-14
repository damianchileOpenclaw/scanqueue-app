#!/bin/bash

# Script para iniciar ScanQueue con enlaces públicos
# Usa la IP pública del servidor

echo "🚀 Iniciando ScanQueue con acceso público..."
echo "============================================"

cd "$(dirname "$0")"

# Obtener IP pública
echo "🌍 Obteniendo IP pública..."
PUBLIC_IP=$(curl -s ifconfig.me)
if [ -z "$PUBLIC_IP" ]; then
    PUBLIC_IP=$(curl -s icanhazip.com)
fi
if [ -z "$PUBLIC_IP" ]; then
    PUBLIC_IP=$(hostname -I | awk '{print $1}')
fi

echo "✅ IP Pública: $PUBLIC_IP"

# Configurar virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creando virtual environment..."
    python3 -m venv venv
fi

# Activar virtual environment
source venv/bin/activate

# Instalar dependencias si es necesario
if [ ! -f "venv/bin/flask" ]; then
    echo "📦 Instalando dependencias..."
    pip install -r requirements.txt --quiet
fi

# Inicializar base de datos
echo "🗄️ Inicializando base de datos..."
python3 -c "
from app import init_db, init_default_queues
init_db()
init_default_queues()
print('✅ Base de datos lista')
" 2>/dev/null || echo "⚠️  Base de datos ya existe"

# Detener servidor si ya está corriendo
echo "🛑 Deteniendo servidor anterior..."
pkill -f "python.*app.py" 2>/dev/null || true
sleep 2

# Iniciar servidor
echo "🌐 Iniciando servidor en puerto 5000..."
python app.py > scanqueue_public.log 2>&1 &
SERVER_PID=$!

echo "⏳ Esperando que el servidor inicie..."
sleep 8

# Verificar si el servidor está corriendo
if curl -s http://localhost:5000/ > /dev/null; then
    echo "✅ Servidor iniciado correctamente (PID: $SERVER_PID)"
else
    echo "❌ No se pudo iniciar el servidor"
    echo "Revisa scanqueue_public.log para detalles"
    exit 1
fi

# Verificar si el puerto es accesible externamente
echo "🔍 Verificando acceso externo..."
if timeout 5 curl -s "http://$PUBLIC_IP:5000/" > /dev/null; then
    echo "✅ Puerto 5000 accesible externamente"
    ACCESSIBLE=true
else
    echo "⚠️  Puerto 5000 no accesible externamente"
    echo "   Puede que necesites configurar el firewall"
    ACCESSIBLE=false
fi

echo ""
echo "🎉 ¡SCANQUEUE LISTO! 🎉"
echo "============================================"
echo ""
echo "🌍 **ENLACES PÚBLICOS:**"
echo ""
echo "📱 **PARA CLIENTES:**"
echo "   🔗 Tomar número:     http://$PUBLIC_IP:5000/customer"
echo "   🏠 Página principal: http://$PUBLIC_IP:5000/"
echo ""
echo "👨‍💼 **PARA ADMINISTRADORES:**"
echo "   🔧 Panel de control: http://$PUBLIC_IP:5000/admin"
echo ""
echo "📊 **MONITOREO:**"
echo "   📈 Dashboard:        http://$PUBLIC_IP:5000/"
echo "   🔌 API Status:       http://$PUBLIC_IP:5000/api/queues"
echo ""
if [ "$ACCESSIBLE" = false ]; then
    echo "⚠️  **ADVERTENCIA:**"
    echo "   Los enlaces pueden no funcionar si:"
    echo "   • El firewall bloquea el puerto 5000"
    echo "   • El proveedor bloquea puertos"
    echo "   • Necesitas configuración NAT"
    echo ""
    echo "🔧 **SOLUCIONES:**"
    echo "   1. Configurar firewall:"
    echo "      sudo ufw allow 5000/tcp"
    echo "   2. Usar reverse proxy (recomendado):"
    echo "      ./deploy.sh (configura Nginx)"
    echo "   3. Usar servicio cloud:"
    echo "      Railway.app, Render.com, etc."
    echo ""
fi

echo "📱 **PARA CÓDIGOS QR:**"
echo "   Ejecuta: python generate_qr_codes.py 'http://$PUBLIC_IP:5000'"
echo ""
echo "🔧 **INFORMACIÓN TÉCNICA:**"
echo "   • IP Pública:      $PUBLIC_IP"
echo "   • Puerto:          5000"
echo "   • PID Servidor:    $SERVER_PID"
echo "   • Logs:           scanqueue_public.log"
echo "   • Local:          http://localhost:5000"
echo ""
echo "🛑 **PARA DETENER:**"
echo "   Ejecuta: pkill -f 'python.*app.py'"
echo "   O: ./stop_public_links.sh"
echo ""
echo "🚀 **PARA PRODUCCIÓN (recomendado):**"
echo "   Usa: ./deploy.sh (configura como servicio)"
echo ""
echo "============================================"
echo "✅ Sistema listo en: http://$PUBLIC_IP:5000"
echo ""

# Guardar información en archivo
cat > PUBLIC_LINKS_IP.txt << EOF
ENLACES PÚBLICOS SCANQUEUE
===========================
Fecha: $(date)
IP Pública: $PUBLIC_IP
Puerto: 5000

ENLACES CLIENTES:
- Página principal: http://$PUBLIC_IP:5000/
- Tomar número: http://$PUBLIC_IP:5000/customer
- Ver estado: http://$PUBLIC_IP:5000/customer (con número)

ENLACES ADMINISTRACIÓN:
- Panel admin: http://$PUBLIC_IP:5000/admin
- API queues: http://$PUBLIC_IP:5000/api/queues

INFORMACIÓN TÉCNICA:
- Servidor local: http://localhost:5000
- PID Servidor: $SERVER_PID
- Logs: scanqueue_public.log

PARA DETENER:
Ejecutar: pkill -f 'python.*app.py'
O: ./stop_public_links.sh

PARA QR CODES:
python generate_qr_codes.py 'http://$PUBLIC_IP:5000'
EOF

echo "📄 URLs guardadas en: PUBLIC_LINKS_IP.txt"

# Generar códigos QR automáticamente
echo ""
echo "🔄 Generando códigos QR..."
python generate_qr_codes.py "http://$PUBLIC_IP:5000"

echo ""
echo "🎯 **RESUMEN FINAL:**"
echo "   1. Clientes usan: http://$PUBLIC_IP:5000/customer"
echo "   2. Admin usa:     http://$PUBLIC_IP:5000/admin"
echo "   3. QR codes en:   qr_codes/"
echo "   4. Para detener:  pkill -f 'python.*app.py'"
echo ""
echo "✅ ¡Listo para usar desde cualquier parte del mundo! 🌎"

# Mantener el script corriendo
echo ""
echo "📡 Servidor activo. Presiona Ctrl+C para detener."
echo ""
wait $SERVER_PID