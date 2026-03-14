# 🚨 SOLUCIÓN DE EMERGENCIA - ScanQueue

## 📋 **PROBLEMA IDENTIFICADO:**
El proveedor de cloud (Tencent Cloud/AWS/etc.) está bloqueando los puertos 5000 y 8080.

## 🎯 **SOLUCIONES DISPONIBLES:**

### **OPCIÓN 1: Usar puerto 80 o 443 (recomendado)**
```bash
# Cambiar puerto en app.py
# Línea final: port=80  o  port=443
```

### **OPCIÓN 2: Configurar Nginx como reverse proxy**
```bash
# Instalar Nginx
sudo apt install nginx

# Configurar proxy
sudo nano /etc/nginx/sites-available/scanqueue
```

### **OPCIÓN 3: Servicio Cloud gratuito (MÁS FÁCIL)**
1. **Railway.app** - Sube el código, ellos manejan todo
2. **Render.com** - Similar a Railway
3. **Fly.io** - Buena opción gratuita

---

## 🚀 **SOLUCIÓN RÁPIDA (AHORA MISMO):**

### **Paso 1: Cambiar a puerto 80**
Edita `app.py`:
```python
# Cambia la última línea:
socketio.run(app, host='0.0.0.0', port=80, allow_unsafe_werkzeug=True)
```

### **Paso 2: Ejecutar como root (puerto 80 necesita permisos)**
```bash
cd scanqueue_app
sudo $(which python) app.py
```

### **Paso 3: Nuevos enlaces**
```
http://43.135.169.86/          # Página principal
http://43.135.169.86/customer  # Clientes
http://43.135.169.86/admin     # Administración
```

---

## 🔧 **SI EL PUERTO 80 TAMBIÉN ESTÁ BLOQUEADO:**

### **Usar Nginx:**
```bash
# 1. Instalar Nginx
sudo apt install nginx

# 2. Crear configuración
sudo tee /etc/nginx/sites-available/scanqueue << 'EOF'
server {
    listen 80;
    server_name _;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /socket.io {
        proxy_pass http://localhost:8080/socket.io;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
EOF

# 3. Activar y reiniciar
sudo ln -s /etc/nginx/sites-available/scanqueue /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 📱 **ENLACES DE PRUEBA (LOCALES):**

Mientras solucionamos el acceso externo, puedes probar **LOCALMENTE**:

### **En tu misma red:**
```
http://[IP-DEL-SERVIDOR]:8080/customer
http://[IP-DEL-SERVIDOR]:8080/admin
```

### **Para generar nueva IP si cambia:**
```bash
curl ifconfig.me
```

---

## 🎯 **SOLUCIÓN DEFINITIVA (RECOMENDADA):**

### **Usar Railway.app (gratis):**
1. Crear cuenta en railway.app
2. Conectar con GitHub (sube el código)
3. Railway te da dominio: `https://tunombre.railway.app`
4. Configurar automáticamente

### **Ventajas:**
- ✅ Dominio HTTPS automático
- ✅ Escalable
- ✅ Sin problemas de puertos
- ✅ Backup automático

---

## 📞 **PASOS INMEDIATOS:**

1. **Prueba local primero:**
   ```bash
   # En el servidor:
   curl http://localhost:8080/customer
   ```

2. **Si funciona localmente:**
   - El problema es de red/firewall
   - Necesitamos abrir puertos o usar proxy

3. **Solución inmediata:**
   - Usar puerto 80 con Nginx
   - O migrar a Railway/Render

---

## 🔍 **DIAGNÓSTICO RÁPIDO:**

Ejecuta esto en el servidor:
```bash
# Verificar si el servidor responde
curl -s http://localhost:8080/ > /dev/null && echo "✅ Servidor OK" || echo "❌ Servidor caído"

# Verificar puertos abiertos
sudo netstat -tulpn | grep :8080

# Verificar firewall
sudo ufw status
```

---

## 🆘 **SI NADA FUNCIONA:**

### **Plan B: Archivos estáticos**
He creado una versión HTML estática que puedes usar MIENTRAS:

1. **Descarga los archivos HTML:**
   - `templates/index.html`
   - `templates/customer.html` 
   - `templates/admin.html`

2. **Súbelos a cualquier hosting:**
   - GitHub Pages (gratis)
   - Netlify (gratis)
   - Vercel (gratis)

3. **Usa esos enlaces temporalmente**

---

## ✅ **RESUMEN:**

**Problema:** Puertos bloqueados por proveedor cloud  
**Solución 1:** Usar puerto 80 con Nginx ✓  
**Solución 2:** Migrar a Railway.app ✓  
**Solución 3:** Archivos estáticos en hosting gratuito ✓  

**¿Cuál prefieres que implemente primero?**