from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import requests
import io
import json

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

# 🔹 Replace with your Azure details
AZURE_SUBSCRIPTION_KEY = "12OraUPwInb9Gb0LyCQycn4uoAxuFRQWLYR1j1aPIe5DiwXDCC5EJQQJ99BBACYeBjFXJ3w3AAAEACOG7sdg"
AZURE_ENDPOINT = "https://hacktest2211.cognitiveservices.azure.com/"  # Example: https://your-region.cognitiveservices.azure.com/
AZURE_DESCRIBE_URL = f"{AZURE_ENDPOINT}/vision/v3.2/describe"
api_user = 928298131
api_secret = 'LRE4cRS3ozowYuqFXZneBdzvPyPLUStx'

# 🔹 API route for URL-based image analysis
@app.post("/analyze/url/")
async def analyze_image_url(image_url: str):
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_SUBSCRIPTION_KEY,
        "Content-Type": "application/json"
    }
    data = {"url": image_url}
    
    response = requests.post(AZURE_DESCRIBE_URL, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return {"description": result["description"]["captions"][0]["text"]}
    else:
        return {"error": response.json()}

# 🔹 API route for local file upload
@app.post("/analyze/upload/")
async def analyze_image_upload(file: UploadFile = File(...)):
    headers = {"Ocp-Apim-Subscription-Key": AZURE_SUBSCRIPTION_KEY}

    image_data = await file.read()

    response = requests.post(AZURE_DESCRIBE_URL, headers=headers, files={"file": io.BytesIO(image_data)})

    if response.status_code == 200:
        result = response.json()
        return {"description": result["description"]["captions"][0]["text"]}
    else:
        return {"error": response.json()}


@app.get("/check_image")
def check_image(url: str):
    params = {
        'url': url,
        'models': 'genai',
        'api_user': api_user,
        'api_secret': api_secret
    }
    r = requests.get('https://api.sightengine.com/1.0/check.json', params=params)
    output = json.loads(r.text)
    return output
