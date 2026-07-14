import requests

while True:
    user=input('You:')
    response=requests.post("http://localhost:8000/agent", json={"text": user})

    print(response.status_code)
    print(response.json())