import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

# ⚠️ Usa tu URL pública del puerto 3030 (HTTPS, sin barra final).
BACKEND_URL = os.getenv(
    "DEALERS_API_URL",
    "https://dannyse2004-3030.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai"
).rstrip("/")

# si no tienes el analizador, devolvemos neutral por defecto
SENTIMENT_URL = os.getenv("SENTIMENT_URL", "").rstrip("/")

def get_request(endpoint, params=None):
    url = f"{BACKEND_URL}{endpoint}"
    try:
        print(f"DEBUG GET → {url} params={params}")
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json()  # /fetchDealers devuelve un ARRAY
    except Exception as e:
        print("ERROR get_request:", url, e)
        return []  # devuelve lista vacía para no romper la vista

def post_review(data_dict):
    url = f"{BACKEND_URL}/insert_review"
    try:
        print(f"DEBUG POST → {url}")
        r = requests.post(url, data=json.dumps(data_dict),
                          headers={"Content-Type": "application/json"},
                          timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print("ERROR post_review:", url, e)
        return {"status": 500, "message": "Internal Server Error"}

def analyze_review_sentiments(text):
    if not SENTIMENT_URL:
        return {"sentiment": "neutral"}
    try:
        url = f"{SENTIMENT_URL}/analyze/{text}"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print("ERROR sentiment:", e)
        return {"sentiment": "neutral"}
