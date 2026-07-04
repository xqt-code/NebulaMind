import requests
import json

url = "http://localhost:8000/api/v1/chat/ask"

payload = {
    "question": "什么是RAG？",
    "tenant_id": "1",
    "stream": False
}

try:
    resp = requests.post(url, json=payload, timeout=10)
    print(f"状态码: {resp.status_code}")
    print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print(f"请求失败: {e}")