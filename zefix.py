import requests
import json

# Your credentials
username = "test"
password = "1234"

# API endpoint
url = "https://www.zefix.admin.ch/ZefixPublicREST/api/v1/company/search.json"

# Headers
headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

# Payload
payload = {
    "name": "Rolex",
    "language": "en"
}

# Make request with authentication
response = requests.post(url, headers=headers, json=payload, auth=(username, password))

# Process response
if response.status_code == 200:
    data = response.json()
    print("Companies found:\n")
    for company in data:
        print(f"Name: {company.get('name')}")
        print(f"UID: {company.get('uid')}")
        print(f"Canton: {company.get('canton')}")
        print(f"Legal Seat: {company.get('legalSeat')}")
        print(f"Company ID: {company.get('companyId')}")
        print("-" * 40)
else:
    print("Request failed.")
    print("Status code:", response.status_code)
    print("Response:", response.text)
