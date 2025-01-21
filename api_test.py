import requests

url = "http://127.0.0.1:8004/trigger_bt"
payload = {
    "task": "Open google and then Naviagte to https://shinobi.security",
    "add_infos": "",
    "url": "https://shinobi.security"
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
    print("\final_dom:")
    print(result["final_dom"])
else:
    print(f"Request failed with status code: {response.status_code}")