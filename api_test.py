import requests

url = "http://127.0.0.1:8004/trigger_bt"
payload = {
    "task": "Open the url https://ambassador-booking-staging.castusdev.co.uk/login and try to login via dummy credentails",
    "add_infos": "In the final result, include the url of the page the task finished at",
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
    print("\Screenshot:")
    print(result["sc"])

else:
    print(f"Request failed with status code: {response.status_code}")