# 🚀 GUÍA PARA DESPLEGAR EN RAILWAY.APP

## 📋 **PASO A PASO (10 minutos):**

### **1. Crear cuenta en Railway**
- Visita: https://railway.app
- Regístrate con GitHub (recomendado)
- Plan gratuito incluye:
  - 500 horas/mes
  - 1GB RAM
  - 1GB disco
  - Dominio `*.railway.app`

### **2. Crear nuevo proyecto**
- Click en "New Project"
- Selecciona "Deploy from GitHub repo"
- Conecta tu cuenta GitHub

### **3. Subir el código**
**Opción A: Subir directamente**
1. Descarga `scanqueue_app.zip` (te lo enviaré)
2. En Railway: "New Project" → "Empty Project"
3. Arrastra el ZIP

**Opción B: Desde GitHub**
1. Crea repositorio en GitHub
2. Sube los archivos
3. Conecta Railway con el repo

### **4. Configurar variables (opcional)**
Railway detecta automáticamente:
- Python 3.12
- Dependencias de `requirements.txt`
- Puerto 5000

### **5. Desplegar**
- Click en "Deploy"
- Espera 2-3 minutos
- ¡Listo!

---

## 🌐 **ENLACES QUE OBTENDRÁS:**

### **Después del despliegue:**
```
https://scanqueue-production.up.railway.app/
https://scanqueue-production.up.railway.app/customer
https://scanqueue-production.up.railway.app/admin
```

### **Dominio personalizable:**
Puedes agregar tu propio dominio:
```
https://tutienda.com/
https://tutienda.com/customer
```

---

## 🔧 **CONFIGURACIÓN AUTOMÁTICA:**

Railway configura automáticamente:
- ✅ HTTPS/SSL
- ✅ Balanceador de carga
- ✅ Monitoreo
- ✅ Logs
- ✅ Auto-escalado
- ✅ Backup de base de datos

---

## 📱 **PARA TUS CLIENTES:**

### **Códigos QR actualizados:**
Una vez tengas el dominio de Railway:
```bash
python generate_qr_codes.py "https://tudominio.railway.app"
```

### **Imprimir y colocar:**
1. QR Clientes: En la entrada
2. QR Admin: En caja/administración
3. QR General: En mostrador

---

## 💾 **BASE DE DATOS:**

### **Railway PostgreSQL (gratis):**
1. En Railway: "New" → "Database"
2. Selecciona PostgreSQL
3. Conecta con tu proyecto
4. Railway maneja backups automáticos

### **O mantener SQLite:**
El sistema ya usa SQLite por defecto.

---

## 🛠️ **SOLUCIÓN DE PROBLEMAS:**

### **Si no despliega:**
```bash
# Verificar logs en Railway
# Revisar requirements.txt
# Probar localmente primero
```

### **Si la base de datos no funciona:**
```bash
# Railway usa variables de entorno
# DATABASE_URL se configura automáticamente
```

### **Si los WebSockets no funcionan:**
Railway soporta WebSockets automáticamente.

---

## 📞 **SOPORTE RAILWAY:**

- **Documentación:** https://docs.railway.app
- **Discord:** https://discord.gg/railway
- **Foros:** https://community.railway.app

---

## 🎯 **VENTAJAS DE RAILWAY:**

1. **Gratis** para empezar
2. **Sin configuración** de puertos/firewall
3. **HTTPS automático**
4. **Escalable** cuando crezcas
5. **Backup automático** de base de datos
6. **Monitoreo** incluido
7. **Dominio personalizable**

---

## 🚀 **INSTRUCCIONES RÁPIDAS:**

### **Para empezar HOY:**
1. **Regístrate** en railway.app (5 min)
2. **Crea proyecto** (2 min)
3. **Sube código** (te ayudo)
4. **Obtén enlaces** (2 min)
5. **Genera QR codes** (1 min)
6. **¡A usar!**

### **Costo:**
- **Gratis** para empezar
- Si creces: desde $5/mes
- Sin sorpresas

---

## 📦 **ARCHIVOS LISTOS:**

Tu proyecto ya tiene:
- ✅ `Procfile` - Para Railway
- ✅ `railway.json` - Configuración
- ✅ `requirements.txt` - Dependencias
- ✅ Código completo
- ✅ QR code generator

---

## 🆘 **¿NECESITAS AYUDA?**

### **Yo puedo:**
1. Preparar el ZIP para subir
2. Guiarte paso a paso
3. Verificar que todo funcione
4. Generar nuevos QR codes

### **Tú necesitas:**
1. Cuenta Railway (gratis)
2. 10 minutos de tiempo
3. ¡Ganas de empezar!

---

## ✅ **RESUMEN FINAL:**

**Problema actual:** Proveedor bloquea puertos  
**Solución:** Railway.app (gratis, sin problemas)  
**Tiempo:** 10 minutos  
**Costo:** $0 para empezar  
**Resultado:** Enlaces públicos funcionando  

**¿Listo para migrar a Railway?** 🚀