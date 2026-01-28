
import requests


headers = {"X-Admin-Token": "1123581321"}
response = requests.get(url="http://192.168.2.116:8000/admin/push", headers=headers)

print(response.json())