
import requests

response = requests.get("http://192.168.2.116:8000/admin/push")

print(response.json())