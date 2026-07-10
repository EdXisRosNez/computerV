from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import shutil
from werkzeug.utils import secure_filename

from app.recon_fac import recon_cara, CARAS_PATH
from app.registrador_asist import registro_asist, get_asist_hoy

app = FastAPI(title="Sistema de Asistencia Facial")

# Define the absolute path to the templates directory
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")

# Mount templates to serve static files (like CSS, JS if separated)
app.mount("/static", StaticFiles(directory=TEMPLATES_DIR), name="static")

class FramePayload(BaseModel):
    image: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serves the main dashboard page."""
    index_path = os.path.join(TEMPLATES_DIR, "index.html")
    if not os.path.exists(index_path):
        return "<html><body><h1>Dashboard HTML not found</h1></body></html>"
    with open(index_path, "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/recognize")
async def recognize_api(payload: FramePayload):
    """
    Recibe una imagen de la webcam y trata de reconocer la cara.
    Si lo hace, registra asistencia.
    """
    name = recon_cara(payload.image)
    if name:
        # Face recognized! Log it.
        logged = registro_asist(name)
        if logged:
            return {"estado": "exitoso", "mensaje": f"¡Bienvenido, {name}! Asistencia registrada.", "name": name}
        else:
            return {"estado": "info", "mensaje": f"Hola {name}, tu asistencia ya fue registrada recientemente.", "name": name}
    
    return {"estado": "error", "mensaje": "Rostro no reconocido", "name": None}

@app.get("/api/asistencias")
async def get_asistencias():
    """
    Devuelve asistencia de hoy
    """
    registros = get_asist_hoy()
    return {"registros": registros}

@app.post("/api/enroll")
async def enroll_user(name: str = Form(...), file: UploadFile = File(...)):
    """
    Registra un nuevo usuario guardando su foto en el directorio faces.
    """
    # Sanitiza el nombre del archivo
    safe_name = secure_filename(name.strip())
    if not safe_name:
        raise HTTPException(estado_code=400, detail="Invalid name")
    
    # Verificar extensión
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png']:
        raise HTTPException(estado_code=400, detail="Solo se permiten imágenes JPG y PNG.")
    
    # Para el nombre final
    safe_filename = f"{safe_name}{ext}"
    file_path = os.path.join(CARAS_PATH, safe_filename)
    
    # Guardado del archivo
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {"estado": "exitoso", "mensaje": f"Usuario {safe_name} registrado correctamente."}
