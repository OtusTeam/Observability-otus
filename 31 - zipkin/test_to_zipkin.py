#!/usr/bin/env python

# pip install requests

import requests
import json
import time
from datetime import datetime

# URL для отправки данных в Zipkin
zipkin_url = "http://127.0.0.1:9411/api/v2/spans"

# Создание простого трейса
def create_trace():
    return [
        {
            "traceId": "1234567890abcdef",
            "id": "abcdef1234567890",
            "name": "my-operation",
            "timestamp": int(time.mktime(datetime.now().timetuple()) * 1000),
            "duration": 500000,
            "localEndpoint": {"serviceName": "python-client"},
            "tags": {
                "http.method": "GET",
                "http.url": "http://example.com"
            }
        }
    ]

# Отправка трейса в Zipkin
def send_trace():
    trace = create_trace()
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.post(zipkin_url, data=json.dumps(trace), headers=headers)
    if response.status_code == 202:
        print("Trace sent successfully to Zipkin")
    else:
        print(f"Failed to send trace: {response.status_code}, {response.text}")

if __name__ == "__main__":
    send_trace()

