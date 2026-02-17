
import requests

headers = {"X-Admin-Token": "00000000"}
response = requests.get(url="http://192.168.2.116:8000/admin/push", headers=headers)

print(response.json())