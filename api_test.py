import requests

url = "http://127.0.0.1:8004/trigger_bt"
# payload = {
#     "task": "Navigate to website http://159.65.235.197:32771/ and login with creds username test and password test",
#     "add_infos": "In the final result, include the url of the page the task finished at",
#     "url": "http://159.65.235.197:32771/",
#     "gbc": True,
# }

#, "--ignore-certificate-errors"

payload = {
    "task": "Try to navigate website to shinobi.security and return the timing for the first available demo",
    "add_infos": "In the final result, include the url of the page the task finished at",
    "url": "https://shinobi.security",
    "gbc": True,
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