import os
import json
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SPLUNK_URL = os.getenv("SPLUNK_URL")
SPLUNK_TOKEN = os.getenv("SPLUNK_TOKEN")
HEADERS = {"Authorization": f"Bearer {SPLUNK_TOKEN}"}

rules_dir = "splunk_rules"

if os.path.exists(rules_dir):
    for filename in os.listdir(rules_dir):
        if filename.endswith(".json"):
            with open(os.path.join(rules_dir, filename), "r") as file:
                rule_data = json.load(file)
                
                # API Adresi düzeltildi (Namespace yetki hatasını önlemek için)
                api_endpoint = f"{SPLUNK_URL}/services/saved/searches"
                
                response = requests.post(api_endpoint, headers=HEADERS, data=rule_data, verify=False)
                
                if response.status_code in [200, 201, 409]: 
                    print(f"[+] UĞURLU: {rule_data['name']} Splunk-a göndərildi.")
                else:
                    print(f"[-] XƏTA: {rule_data['name']} xəta verdi. Detal: {response.text}")
