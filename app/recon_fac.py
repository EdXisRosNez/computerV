import os
import cv2
import numpy as np
import base64
from deepface import DeepFace

CARAS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "faces")

# Asegurar que la ruta existe
os.makedirs(CARAS_PATH, exist_ok=True)

def decode_base64_image(base64_string: str) -> np.ndarray:
    """
    Decodes a base64 string to an OpenCV image (numpy array).
    """
    # Quita el header si viene en la cadena
    if "," in base64_string:
        base64_string = base64_string.split(",")[1]
    
    img_data = base64.b64decode(base64_string)
    np_arr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img

def recon_cara(base64_image: str) -> str:
    """
    Attempts to recognize the face in the provided base64 image against the faces directory.
    Returns the name of the recognized person (derived from filename), or None if not recognized/no face found.
    """
    # Por si noy hay caras
    enrolled_files = [f for f in os.listdir(CARAS_PATH) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not enrolled_files:
        return None

    img_array = decode_base64_image(base64_image)
    if img_array is None:
        return None

    try:
        dfs = DeepFace.find(
            img_path=img_array, 
            db_path=CARAS_PATH, 
            enforce_detection=False,
            silent=True,
            detector_backend="mtcnn"
        )

        if len(dfs) > 0 and not dfs[0].empty:
            # Ruta de la cara detectada
            matched_path = dfs[0].iloc[0]["identity"]
            # Obtener el nombre
            basename = os.path.basename(matched_path)
            name, _ = os.path.splitext(basename)
            return name
        return None
    except Exception as e:
        print(f"Error during recognition: {e}")
        return None
