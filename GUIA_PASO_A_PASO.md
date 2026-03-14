# 🚀 GUÍA PASO A PASO - SUBIR SCANQUEUE A RAILWAY

## 📋 **ANTES DE EMPEZAR**

### **Lo que necesitas:**
1. ✅ Una cuenta de **GitHub** (gratis)
2. ✅ Una cuenta de **Railway.app** (gratis)
3. ✅ El archivo ZIP: `scanqueue_railway.zip` (48 KB)

### **Tiempo estimado:** 10-15 minutos

---

## 📸 **PASO 1: CREAR CUENTA EN RAILWAY**

1. **Ve a:** https://railway.app/
2. Haz clic en **"Start a New Project"**
3. Selecciona **"Login with GitHub"**

<qqimg>https://i.imgur.com/placeholder1.png</qqimg>
*Nota: Usa tu cuenta de GitHub para registrarte*

---

## 📸 **PASO 2: CREAR NUEVO PROYECTO**

1. En el dashboard de Railway, haz clic en **"New Project"**
2. Selecciona **"Deploy from GitHub repo"**

<qqimg>https://i.imgur.com/placeholder2.png</qqimg>
*Elige la opción de GitHub*

---

## 📸 **PASO 3: SUBIR ARCHIVOS A GITHUB**

### **Opción A: Si ya tienes GitHub Desktop**
1. Crea un nuevo repositorio llamado `scanqueue-app`
2. Extrae el ZIP `scanqueue_railway.zip`
3. Sube todos los archivos al repositorio

### **Opción B: Desde la web de GitHub**
1. Ve a https://github.com/new
2. Nombre: `scanqueue-app`
3. Marca **"Add a README file"**
4. Haz clic en **"Upload files"**
5. Arrastra todos los archivos del ZIP

<qqimg>https://i.imgur.com/placeholder3.png</qqimg>
*Sube los archivos a GitHub*

---

## 📸 **PASO 4: CONECTAR GITHUB CON RAILWAY**

1. En Railway, busca tu repositorio `scanqueue-app`
2. Haz clic en **"Deploy"**

<qqimg>https://i.imgur.com/placeholder4.png</qqimg>
*Selecciona tu repositorio*

---

## 📸 **PASO 5: ESPERAR EL DESPLIEGUE**

Railway comenzará automáticamente:
- ✅ Instalar Python 3.12
- ✅ Instalar dependencias (Flask, etc.)
- ✅ Configurar el servidor
- ✅ Asignar un dominio público

<qqimg>https://i.imgur.com/placeholder5.png</qqimg>
*Verás el progreso en tiempo real*

---

## 📸 **PASO 6: OBTENER TU DOMINIO**

Una vez completado, verás:
```
✅ Deployment successful
🌐 Domain: https://scanqueue-app-production.up.railway.app
```

**Copia este dominio** - ¡es tu URL pública!

<qqimg>https://i.imgur.com/placeholder6.png</qqimg>
*Tu dominio público gratuito*

---

## 📸 **PASO 7: PROBAR LA APLICACIÓN**

### **Abre estos enlaces:**

1. **Para clientes:**
```
https://scanqueue-app-production.up.railway.app/customer
```

2. **Para administradores:**
```
https://scanqueue-app-production.up.railway.app/admin
```

3. **Página principal:**
```
https://scanqueue-app-production.up.railway.app/
```

<qqimg>https://i.imgur.com/placeholder7.png</qqimg>
*Interfaz de cliente funcionando*

---

## 📸 **PASO 8: GENERAR NUEVOS QR CODES**

### **Desde tu computadora:**
```bash
# Descarga el proyecto
git clone https://github.com/tu-usuario/scanqueue-app.git
cd scanqueue-app

# Genera QR codes con tu nuevo dominio
python generate_qr_codes.py --url https://scanqueue-app-production.up.railway.app
```

### **O desde Railway (consola):**
1. Ve a la pestaña **"Console"** en Railway
2. Ejecuta:
```bash
python generate_qr_codes.py --url https://scanqueue-app-production.up.railway.app
```

<qqimg>/root/.openclaw/workspace/scanqueue_app/qr_codes/qr_combinado.png</qqimg>
*Ejemplo de códigos QR generados*

---

## 📸 **PASO 9: CONFIGURACIÓN AVANZADA (OPCIONAL)**

### **Variables de entorno:**
En Railway → Settings → Variables:
```
FLASK_ENV=production
SECRET_KEY=tu-clave-secreta
```

### **Dominio personalizado:**
1. Ve a **Settings** → **Domains**
2. Agrega tu dominio (ej: `queue.tuempresa.com`)
3. Configura los DNS

---

## 🆘 **SOLUCIÓN DE PROBLEMAS**

### **Problema 1: "ModuleNotFoundError: No module named 'flask'"**
**Solución:** Railway instala automáticamente las dependencias. Si falla, revisa el archivo `requirements.txt`.

### **Problema 2: "Application failed to start"**
**Solución:** Revisa los logs en Railway → **Logs**.

### **Problema 3: "WebSocket connection failed"**
**Solución:** Railway soporta WebSocket automáticamente. Asegúrate de usar HTTPS.

### **Problema 4: "Puerto no disponible"**
**Solución:** Railway usa el puerto definido en `$PORT`. Ya está configurado en `app.py`.

---

## ✅ **VERIFICACIÓN FINAL**

### **Prueba estos endpoints:**
```bash
# 1. Página principal (debe devolver HTML)
curl https://scanqueue-app-production.up.railway.app/

# 2. API de colas (debe devolver JSON)
curl https://scanqueue-app-production.up.railway.app/api/queues

# 3. WebSocket (debe conectarse)
# Abre la consola del navegador y verifica
```

---

## 📞 **SOPORTE**

### **Si necesitas ayuda:**
1. **Railway Discord:** https://discord.gg/railway
2. **Documentación:** https://docs.railway.app/
3. **Comunidad GitHub:** https://github.com/railwayapp

### **Contacto rápido:**
- **Problemas técnicos:** Revisa los logs en Railway
- **Configuración:** Modifica `config.py` y redepleya
- **Personalización:** Edita los archivos en `templates/`

---

## 🎉 **¡FELICIDADES!**

Tu sistema ScanQueue ahora está:
✅ **En línea 24/7**  
✅ **Con dominio público**  
✅ **Con SSL/TLS (HTTPS)**  
✅ **Escalable automáticamente**  
✅ **Gratis para empezar**  

**¡Listo para usar en tu negocio!** 🚀

---

## 📱 **QR CODES PARA IMPRIMIR**

<qqimg>/root/.openclaw/workspace/scanqueue_app/qr_codes/qr_cliente.png</qqimg>
**PARA CLIENTES** - Escanear para tomar número

<qqimg>/root/.openclaw/workspace/scanqueue_app/qr_codes/qr_admin.png</qqimg>
**PARA ADMINISTRADORES** - Panel de control

<qqimg>/root/.openclaw/workspace/scanqueue_app/qr_codes/qr_inicio.png</qqimg>
**PÁGINA PRINCIPAL** - Monitor en tiempo real