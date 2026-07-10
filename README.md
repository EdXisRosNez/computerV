# 📷 Sistema de Asistencia Automatizada con Reconocimiento Facial

Un sistema automatizado e inteligente diseñado para detectar y registrar automáticamente la asistencia de personas mediante reconocimiento facial en tiempo real a través de una cámara web.

Impulsado por **FastAPI** en el backend y **DeepFace** para la inferencia de reconocimiento facial, este sistema elimina la necesidad de registros manuales y credenciales, agilizando el control de asistencia.

---

## 🚀 Características Principales

* **Detección y Reconocimiento en Tiempo Real:** Identifica rostros de forma fluida a través de la alimentación de video.
* **Registro Automático de Asistencia:** Registra la hora exacta de entrada de los usuarios reconocidos (ej. en un archivo CSV o base de datos).
* **Gestión de Usuarios (Enrollment):** Capacidad para registrar rostros nuevos y vincularlos a la identidad de una persona.
* **Interfaz de Usuario Intuitiva:** Dashboard interactivo para visualizar el feed de la cámara y el registro diario de asistencias.

---

## 🛠️ Tecnologías Utilizadas

* **FastAPI:** Backend robusto y de alto rendimiento.
* **DeepFace:** Framework avanzado de reconocimiento facial y análisis para Python.
* **OpenCV (opencv-python-headless):** Captura y procesamiento del flujo de imágenes.
* **HTML5 / CSS / JavaScript:** Frontend interactivo y moderno.

---

## ⚙️ Instalación y Configuración

El proyecto contiene un script automatizado para levantar el entorno y el servidor fácilmente:

### 1. Navegar al Directorio del Proyecto
```bash
cd computerV
```

### 2. Arrancar la Aplicación
Ejecuta el script de inicio (asegúrate de darle permisos de ejecución si es necesario con `chmod +x start.sh`):
```bash
./start.sh
```
*Este script creará automáticamente el entorno virtual, instalará las dependencias de `requirements.txt` y lanzará el servidor local.*

### 3. Abrir el Navegador
Una vez que el servidor reporte estar listo, abre tu navegador en:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

> 💡 **Nota de Primera Ejecución**: La primera vez que el sistema intente reconocer un rostro, DeepFace descargará automáticamente los modelos neuronales (VGG-Face, MTCNN, etc.). Este proceso ocurre una sola vez y tomará algunos segundos según tu conexión.

---

## 🔧 Solución de Problemas Frecuentes

### Error: `cv2 has no attribute 'CascadeClassifier'` o falta `haarcascade_frontalface_default.xml`
Si configuras el motor de detección en modo `opencv` y te encuentras con un error indicando que falta el archivo XML de Haar Cascade, puedes solucionarlo descargando manualmente el archivo en tu entorno virtual. Ejecuta el siguiente comando en la raíz del proyecto:

```bash
wget https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml -O .venv/lib/python3.12/site-packages/cv2/data/haarcascade_frontalface_default.xml
```
*Nota: Actualmente el sistema utiliza **MTCNN** como detector por defecto para evitar este problema y mejorar la precisión, por lo que no deberías toparte con este error a menos que reviertas a OpenCV.*
