import os
import requests
from datetime import datetime

GENDER = "male"
WEIGHT_KG = 63
HEIGHT_CM = 174
AGE = 25

APP_ID= os.environ.get("APP_ID")
API_KEY= os.environ.get("API_KEY")
TOKEN = os.environ.get('TOKEN')
nutrition_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
SHEET_ENDPOINT = os.environ.get("SHEET_ENDPOINT")


nutrition_text = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}
parameter = {
    "query": nutrition_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}
response = requests.post(nutrition_endpoint, json=parameter, headers=headers)
data = response.json()
print(data)

bearer_headers = {
    "Authorization": f"Bearer {os.environ.get('TOKEN')}"
}

today = datetime.now()
today_date = today.strftime("%d/%m/%Y")
today_time = today.strftime("%X")


for exercise in data["exercises"]:
    sheet_parameter = {
        "workout": {
            "date": today_date,
            "time": today_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }

    response = requests.post(SHEET_ENDPOINT, json=sheet_parameter, headers=bearer_headers)
    print(response.text)
