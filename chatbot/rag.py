import re
import requests
from django.conf import settings


def generar_respuesta(prompt: str, pregunta: str, modelo: str, engine: str, n_predict: int = 384, temperatura: float = 0.8):
    if engine == "groq":
        url = f"{settings.GROQ_API}"
        headers = {
            "Content-Type":"application/json",
            "Authorization": f"Bearer {settings.GROQ_KEY}"
        }
    elif engine == "openrouter":
        url = f"{settings.OR_API}"
        headers = {
                    "Content-Type":"application/json",
                    "Authorization": f"Bearer {settings.OR_KEY}"
                }
    else: url = f"{settings.LLAMACPP_API}"
    payload = {
        "model": modelo,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": pregunta}
        ],
        "max_tokens": n_predict,
        "temperature": temperatura,
        "stream": False,
        "stop": ["Usuario:", "Pregunta:"],
    }
    
    print("haciendo peticion a: ", url)
    resp = requests.post(url, json=payload, timeout=900, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return limpiar_respuesta(data["choices"][0]["message"]["content"])

def limpiar_respuesta(respuesta: str):
    texto = re.sub(r"```+", "", respuesta)
    # Quita espacios al inicio y fin de línea
    texto = texto.strip()

    if texto.startswith("=== RESPUESTA ===\n"):
        texto = texto.replace("=== RESPUESTA ===\n", "")
    if texto.startswith("===\nRespuesta ===\n"):
        texto = texto.replace("===\nRespuesta ===\n", "")
    if texto.startswith("=== RESPUESTA\n"):
        texto = texto.replace("=== RESPUESTA\n", "")
    if texto.startswith("===\nRespuesta\nHistorial relevante:\n"):
        texto = texto.replace("===\nRespuesta\nHistorial relevante:\n", "")
    if texto.startswith("Asistente: "):
        texto = texto.replace("Asistente: ", "").strip()
    if texto.startswith("Asistente:\n"):
        texto = texto.replace("Asistente:\n", "").strip()

    return texto.replace("===\nRespuesta\nHistorial relevante:\n", "")

def generar_respuesta_google(prompt: str, pregunta: str, modelo: str, n_predict: int = 384, temperatura: float = 0.8):
    url = f"https://generativelanguage.googleapis.com/v1/models/{modelo}:generateContent"
    headers = {
        "Content-Type":"application/json",
        "x-goog-api-key": settings.GOOGLE_KEY
    }
    prompt = prompt.join(f"""\n
        Pregunta del Usuario: {pregunta}\n
    """)
    payload = {
        "contents": [{
        "parts": [{"text": prompt}]
        }
        ],
        "generationConfig": {
            "temperature": temperatura
        }
    }
    print("haciendo peticion a: ", url)
    resp = requests.post(url, json=payload, timeout=900, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]