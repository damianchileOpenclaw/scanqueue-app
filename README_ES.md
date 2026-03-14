# ScanQueue - Sistema de Colas en Línea

## Descripción
Un sistema completo de gestión de colas en línea que permite a los clientes tomar números de espera y recibir notificaciones en tiempo real sin necesidad de hacer fila física.

## Características Principales

### Para Clientes
- 📱 **Tomar número**: Escanear código QR o acceder a la página web
- 🔔 **Notificaciones en tiempo real**: Progreso de la cola, aviso cuando sea su turno
- 📊 **Estado de la cola**: Ver número de personas esperando, tiempo estimado
- ⏰ **Espera remota**: No es necesario estar presente físicamente

### Para Administradores
- 🎯 **Gestión de llamadas**: Llamar números, saltar, completar servicios
- 📈 **Monitoreo de colas**: Ver estado de todas las colas en tiempo real
- 📊 **Análisis de datos**: Estadísticas de tiempos de espera, flujo de clientes
- ⚙️ **Configuración del sistema**: Crear y gestionar diferentes colas

### Características Técnicas
- 🌐 **Diseño responsive**: Compatible con móviles, tablets y computadoras
- 🔄 **Actualización en tiempo real**: Comunicación WebSocket
- 📱 **Notificaciones multi-plataforma**: SMS, WeChat, notificaciones push
- 🗄️ **Base de datos**: SQLite (para desarrollo) / MySQL/PostgreSQL (para producción)

## Instalación Rápida

### Requisitos
- Python 3.8 o superior
- Navegador web moderno
- Conexión a Internet

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
```bash
git clone <url-del-repositorio>
cd scanqueue_app
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Inicializar la base de datos**
```bash
python3 -c "from app import init_db, init_default_queues; init_db(); init_default_queues()"
```

4. **Ejecutar el servidor**
```bash
python app.py
```

5. **Acceder al sistema**
   - Página de clientes: `http://localhost:5000/customer`
   - Panel de administración: `http://localhost:5000/admin`
   - Página principal: `http://localhost:5000/`

## Despliegue en Producción

### Opción 1: Servidor Dedicado
```bash
# Dar permisos de ejecución al script de despliegue
chmod +x deploy.sh

# Ejecutar despliegue
./deploy.sh
```

### Opción 2: Docker (Recomendado)
```dockerfile
# Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

### Opción 3: Servicios en la Nube
- **AWS**: EC2 + RDS + Elastic Beanstalk
- **Google Cloud**: Compute Engine + Cloud SQL
- **Azure**: App Service + Azure SQL
- **Tencent Cloud**: Lighthouse + TencentDB

## Configuración

### Archivos de Configuración
1. `app.py` - Configuración principal del servidor
2. `scanqueue.db` - Base de datos SQLite
3. `requirements.txt` - Dependencias de Python

### Variables de Entorno (Opcional)
```bash
export FLASK_SECRET_KEY='tu-clave-secreta'
export DATABASE_URL='mysql://usuario:contraseña@localhost/scanqueue'
export PORT=5000
```

## Uso del Sistema

### Para Clientes
1. Escanear el código QR o visitar la URL
2. Seleccionar el tipo de servicio
3. Tomar número de espera
4. Recibir notificaciones cuando sea su turno

### Para Empleados
1. Acceder al panel de administración
2. Seleccionar la cola correspondiente
3. Llamar números cuando estén disponibles
4. Marcar como completado cuando termine el servicio

## Escenarios de Uso

### 1. Restaurantes y Cafeterías
- Clientes toman número para mesa
- Reciben notificación cuando su mesa está lista
- Pueden esperar en otras áreas del establecimiento

### 2. Hospitales y Clínicas
- Pacientes toman número para consulta
- Sistema muestra tiempo estimado de espera
- Reducción de aglomeraciones en salas de espera

### 3. Oficinas Gubernamentales
- Ciudadanos toman número para trámites
- Sistema de colas organizado por tipo de servicio
- Mejora en la experiencia del usuario

### 4. Tiendas Minoristas
- Clientes toman número para atención personalizada
- Especial atención durante promociones y ventas
- Gestión eficiente del personal de ventas

## Características Avanzadas

### 1. Notificaciones Multi-canal
- Notificaciones en navegador
- Mensajes SMS (requiere integración con proveedor)
- Notificaciones push en aplicación móvil
- Integración con WeChat (para China)

### 2. Análisis y Reportes
- Tiempos promedio de espera
- Picos de demanda por hora/día
- Eficiencia del personal
- Satisfacción del cliente (encuestas integradas)

### 3. Personalización
- Logo y colores personalizables
- Múltiples idiomas
- Diferentes tipos de colas
- Reglas de prioridad personalizables

## Seguridad

### Medidas Implementadas
- ✅ Autenticación para panel de administración
- ✅ Base de datos cifrada
- ✅ Protección contra ataques comunes
- ✅ Logs de auditoría

### Mejores Prácticas
1. **En producción**, usar base de datos externa (MySQL/PostgreSQL)
2. **Configurar HTTPS** para todas las comunicaciones
3. **Implementar backup automático** de la base de datos
4. **Monitorear logs** regularmente

## Soporte y Mantenimiento

### Solución de Problemas Comunes
1. **Servidor no inicia**: Verificar puerto 5000 disponible
2. **Base de datos corrupta**: Restaurar desde backup
3. **Notificaciones no funcionan**: Verificar configuración WebSocket
4. **Acceso lento**: Optimizar consultas a base de datos

### Actualizaciones
```bash
# Actualizar código
git pull origin main

# Actualizar dependencias
pip install -r requirements.txt --upgrade

# Reiniciar servicio
systemctl restart scanqueue
```

## Contribución

### Reportar Problemas
1. Crear issue en GitHub
2. Describir el problema detalladamente
3. Incluir pasos para reproducir
4. Adjuntar logs relevantes

### Desarrollo
1. Fork el repositorio
2. Crear rama para la funcionalidad
3. Implementar cambios
4. Crear Pull Request

## Licencia
Este proyecto está bajo licencia MIT. Ver archivo LICENSE para más detalles.

## Contacto
- **Soporte técnico**: support@scanqueue.com
- **Documentación**: docs.scanqueue.com
- **Comunidad**: community.scanqueue.com

---

**¡Gracias por usar ScanQueue!** 🎉

*Sistema desarrollado para mejorar la experiencia de espera y optimizar la gestión de colas en establecimientos comerciales y de servicios.*