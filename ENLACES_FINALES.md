# 🌐 ENLACES PÚBLICOS SCANQUEUE

## 🎯 **ENLACES PRINCIPALES**

### 📱 **PARA TUS CLIENTES:**
```
http://43.135.169.86:5000/customer
```
**Qué hace:** Los clientes pueden tomar número, ver estado de la cola, recibir notificaciones.

### 👨‍💼 **PARA ADMINISTRADORES:**
```
http://43.135.169.86:5000/admin
```
**Qué hace:** Tu personal puede llamar números, gestionar colas, ver estadísticas.

### 🏠 **PÁGINA PRINCIPAL:**
```
http://43.135.169.86:5000/
```
**Qué hace:** Dashboard general del sistema.

---

## 📋 **CÓMO USAR:**

### **1. Para Clientes:**
1. Visitar: `http://43.135.169.86:5000/customer`
2. Seleccionar tipo de servicio
3. Tomar número
4. Esperar notificación cuando sea su turno

### **2. Para Administradores:**
1. Visitar: `http://43.135.169.86:5000/admin`
2. Seleccionar cola
3. Llamar números cuando estén disponibles
4. Marcar como completado

---

## 📱 **CÓDIGOS QR GENERADOS:**

He generado códigos QR automáticamente. Encuéntralos en:
```
scanqueue_app/qr_codes/
```
- `qr_cliente.png` - Para que los clientes escaneen
- `qr_admin.png` - Para tu personal
- `qr_inicio.png` - Página principal
- `visualizar_qr.html` - Vista web de todos los QR

---

## 🔧 **PARA INICIAR EL SISTEMA:**

```bash
cd scanqueue_app
./start_public.sh
```

**O manualmente:**
```bash
cd scanqueue_app
source venv/bin/activate
python app.py
```

---

## ⚠️ **IMPORTANTE:**

### **Si los enlaces no funcionan:**
1. **Verifica que el servidor esté corriendo:**
   ```bash
   cd scanqueue_app
   ./start_public.sh
   ```

2. **Problemas comunes:**
   - Firewall bloqueando puerto 5000
   - Proveedor bloquea puertos
   - Necesita configuración NAT

3. **Soluciones:**
   ```bash
   # Abrir puerto en firewall (si usas ufw)
   sudo ufw allow 5000/tcp
   
   # Usar puerto diferente (ej: 8080)
   # Edita app.py y cambia port=5000 a port=8080
   ```

---

## 🚀 **PARA PRODUCCIÓN (RECOMENDADO):**

### **Opción A: Servidor Dedicado**
```bash
cd scanqueue_app
./deploy.sh  # Configura como servicio
```

### **Opción B: Servicios Cloud Gratuitos**
- **Railway.app** - Fácil despliegue
- **Render.com** - Gratis con límites
- **Fly.io** - Buena opción

### **Opción C: Dominio Personalizado**
1. Compra dominio (ej: mitienda.com)
2. Configura DNS apuntando a `43.135.169.86`
3. Usa `./deploy.sh` con Nginx

---

## 📞 **SOPORTE RÁPIDO:**

### **Problema: "No se puede acceder"**
**Solución:** 
```bash
# 1. Verifica si el servidor está corriendo
ps aux | grep python

# 2. Inicia el servidor
cd scanqueue_app && ./start_public.sh

# 3. Prueba localmente
curl http://localhost:5000/
```

### **Problema: "Error en página"**
**Solución:**
```bash
# Revisa logs
cd scanqueue_app && tail -f scanqueue_public.log

# Reinicia
pkill -f "python.*app.py"
cd scanqueue_app && ./start_public.sh
```

---

## 🎨 **PERSONALIZACIÓN:**

### **Cambiar nombres de colas:**
Edita `app.py`, busca `DEFAULT_QUEUES`:
```python
DEFAULT_QUEUES = [
    {'name': 'Caja 1', 'description': 'Atención general'},
    {'name': 'Caja 2', 'description': 'Pagos rápidos'},
    {'name': 'Asesoría', 'description': 'Atención personalizada'}
]
```

### **Cambiar colores:**
Edita los archivos HTML en `templates/`

---

## 📊 **ESTADÍSTICAS Y BACKUP:**

### **Base de datos:**
```
scanqueue_app/scanqueue.db
```

### **Backup automático:**
```bash
# Copia manual
cp scanqueue.db scanqueue_backup_$(date +%Y%m%d).db

# Restaurar
cp scanqueue_backup_YYYYMMDD.db scanqueue.db
```

---

## ✅ **VERIFICACIÓN FINAL:**

1. ✅ Sistema creado: **ScanQueue Online**
2. ✅ Funcionalidades completas
3. ✅ Enlaces públicos generados
4. ✅ Códigos QR creados
5. ✅ Documentación incluida

---

## 🌎 **¡TU SISTEMA ESTÁ LISTO!**

**Enlaces activos:**
- 👤 Clientes: `http://43.135.169.86:5000/customer`
- 👨‍💼 Admin: `http://43.135.169.86:5000/admin`
- 🏠 Inicio: `http://43.135.169.86:5000/`

**Próximos pasos:**
1. Prueba los enlaces desde tu móvil
2. Imprime los códigos QR
3. Entrena a tu personal
4. ¡Comienza a usar el sistema!

---

**¿Necesitas ayuda adicional?** ¡Estoy aquí para ayudarte! 🚀