#!/bin/bash

# Script para detener los enlaces públicos de ScanQueue

echo "🛑 Deteniendo enlaces públicos de ScanQueue..."
echo "=============================================="

# Detener procesos de ngrok
echo "🔗 Deteniendo ngrok..."
pkill -f "ngrok http" 2>/dev/null || true
pkill ngrok 2>/dev/null || true

# Detener servidor ScanQueue
echo "🌐 Deteniendo servidor ScanQueue..."
pkill -f "python.*app.py" 2>/dev/null || true

# Esperar un momento
sleep 2

# Verificar que los procesos se detuvieron
if pgrep -f "python.*app.py" > /dev/null; then
    echo "⚠️  Algunos procesos del servidor aún están activos"
    pkill -9 -f "python.*app.py" 2>/dev/null || true
fi

if pgrep ngrok > /dev/null; then
    echo "⚠️  Algunos procesos de ngrok aún están activos"
    pkill -9 ngrok 2>/dev/null || true
fi

# Mostrar resumen
echo ""
echo "📊 RESUMEN DE PROCESOS DETENIDOS:"
echo "----------------------------------"
echo "✅ Ngrok:      $(pgrep ngrok | wc -l) procesos activos"
echo "✅ ScanQueue:  $(pgrep -f "python.*app.py" | wc -l) procesos activos"
echo ""

# Mostrar logs si existen
if [ -f "scanqueue.log" ]; then
    echo "📄 Últimas líneas del log del servidor:"
    tail -5 scanqueue.log
    echo ""
fi

if [ -f "ngrok.log" ]; then
    echo "📄 Últimas líneas del log de ngrok:"
    tail -5 ngrok.log
    echo ""
fi

echo "🎯 Todos los enlaces públicos han sido detenidos"
echo "🔒 El sistema ya no es accesible desde Internet"
echo ""
echo "💡 Para volver a iniciar: ./setup_public_links.sh"
echo "🚀 Para despliegue permanente: ./deploy.sh"