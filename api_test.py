import requests

url = "http://127.0.0.1:8004/trigger_bt"
payload = {
    "task": "Navigate to the login page and inspect the login form fields for email and password.",
    "add_infos": "",
    "url": "https://ambassador-booking-staging.castusdev.co.uk/login"
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    result = response.json()
    print("Final Result:")
    print(result["final_result"])
    print("\nErrors:")
    print(result["errors"])
    print("\nModel Actions:")
    print(result["model_actions"])
else:
    print(f"Request failed with status code: {response.status_code}")