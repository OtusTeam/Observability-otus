import requests
from flask import Flask
import random

app = Flask(__name__)

SERVICE_NAME = "service1"  
SERVICE_PORT = 5001

@app.route('/metrics')
def metrics():
    value = random.randint(0, 100)
    return f'test_metric{{service="{SERVICE_NAME}"}} {value}\n'


def register_to_consul():
    consul_url = "http://consul:8500/v1/agent/service/register"
    payload = {
        "Name": SERVICE_NAME,
        "Address": "service1",
        "Port": SERVICE_PORT,
        "Check": {
            "HTTP": f"http://service1:5001/metrics",
            "Interval": "10s"
        }
    }
    try:
        response = requests.put(consul_url, json=payload)
        if response.status_code == 200:
            print(f"{SERVICE_NAME} зарегистрирован в Consul")
        else:
            print(f"Ошибка регистрации в Consul: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Не удалось зарегистрировать {SERVICE_NAME} в Consul: {e}")

if __name__ == '__main__':
    register_to_consul()
    app.run(host='0.0.0.0', port=5001)
