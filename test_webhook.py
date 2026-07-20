import hmac
import hashlib
import requests
import json


# Webhook URL
URL = "https://biggest-capability-edinburgh-philip.trycloudflare.com/webhooks/inbound"


# Same secret as FastAPI webhook
SECRET = "my_webhook_secret_123"


# Data coming from external system
payload = {
    "customer_id": 2,
    "property_id": 4,
    "status": "new"
}


# Convert payload to bytes
body = json.dumps(payload).encode()


# Create HMAC SHA256 signature
signature = hmac.new(
    SECRET.encode(),
    body,
    hashlib.sha256
).hexdigest()


# Send webhook request
response = requests.post(
    URL,
    headers={
        "x-webhook-signature": signature
    },
    json=payload
)


# Print response
print(
    "Status:",
    response.status_code
)


print(
    "Response:",
    response.json()
)