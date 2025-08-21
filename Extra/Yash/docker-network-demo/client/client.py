import time
import requests

server_url = "http://server:8000"

for i in range(5):
    try:
        response = requests.get(server_url)
        print("Response from server:", response.text)
    except Exception as e:
        print("Server not reachable:", e)
    time.sleep(5)
