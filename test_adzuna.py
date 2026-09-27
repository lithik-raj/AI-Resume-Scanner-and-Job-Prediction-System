import os
import requests
from dotenv import load_dotenv

load_dotenv()

app_id = os.getenv("ADZUNA_APP_ID")
app_key = os.getenv("ADZUNA_APP_KEY")

url = "https://api.adzuna.com/v1/api/jobs/in/search/1"

params = {
    "app_id": app_id,
    "app_key": app_key,
    "results_per_page": 5,
    "what": "machine learning",
    "where": "Bangalore",
    "content-type": "application/json"
}

response = requests.get(url, params=params, timeout=15)

print("Status:", response.status_code)

if response.status_code == 200:
    data = response.json()

    print("\nAPI CONNECTION SUCCESSFUL!")
    print("Jobs found:", len(data.get("results", [])))

    for job in data.get("results", []):
        print("\nJob:", job.get("title"))
        print("Company:", job.get("company", {}).get("display_name"))
        print("Location:", job.get("location", {}).get("display_name"))
        print("Apply:", job.get("redirect_url"))

else:
    print("\nAPI CONNECTION FAILED")
    print(response.text)