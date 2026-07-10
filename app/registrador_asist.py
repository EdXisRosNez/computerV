import csv
import os
from datetime import datetime
from typing import List, Dict

ASISTENCIA_RUTA = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "asistencias.csv")

# Asegurarse que la carpeta existe
os.makedirs(os.path.dirname(ASISTENCIA_RUTA), exist_ok=True)

# Inicializar el archivo CSV con encabezados si no existe
if not os.path.exists(ASISTENCIA_RUTA):
    with open(ASISTENCIA_RUTA, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Date", "Time"])

def registro_asist(name: str) -> bool:
    now = datetime.now()
    today_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")

    # Anti-spam: Verificar si el usuario se registró recientemente (hace 5 mins máximo)
    if os.path.exists(ASISTENCIA_RUTA):
        with open(ASISTENCIA_RUTA, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            # Lee los registros de hoy
            recent_logs = [row for row in reader if row["Name"] == name and row["Date"] == today_date]
            if recent_logs:
                last_log = recent_logs[-1]
                last_time = datetime.strptime(last_log["Time"], "%H:%M:%S")

                # Calcula la diferencia de tiempo
                current_dt = datetime.strptime(current_time, "%H:%M:%S")
                delta = current_dt - last_time
                if delta.total_seconds() < 300: # 5 minutos máximo
                    return False

    # Registra la nueva entrada
    with open(ASISTENCIA_RUTA, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([name, today_date, current_time])
    return True

def get_asist_hoy() -> List[Dict]:
    """
    Devuelve todos los registros de asistencia de hoy.
    """
    now = datetime.now()
    today_date = now.strftime("%Y-%m-%d")
    records = []
    
    if os.path.exists(ASISTENCIA_RUTA):
        with open(ASISTENCIA_RUTA, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Date"] == today_date:
                    records.append({
                        "name": row["Name"],
                        "time": row["Time"]
                    })
    # Return reversed to show latest first
    return records[::-1]
