
import requests
import os


headers = {"X-Admin-Token": os.environ.get("ADMIN_TOKEN")}
response = requests.get(url="http://192.168.2.116:8000/admin/push", headers=headers)

print(response.json())