
import requests

headers = {"X-Admin-Token": "12345678"}
response = requests.post(url="http://192.168.2.116:8000/admin/push", headers=headers)

print(response.json())