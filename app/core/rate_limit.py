from fastapi import Request, HTTPException
from collections import defaultdict
import time


request_history = defaultdict(list)


def rate_limiter(request: Request):

    client_ip = request.client.host

    current_time = time.time()

    limit = 50000
    window = 60

    # Remove old requests
    request_history[client_ip] = [
        timestamp
        for timestamp in request_history[client_ip]
        if current_time - timestamp < window
    ]

    # Check limit
    if len(request_history[client_ip]) >= limit:
        raise HTTPException(
            status_code=429,
            detail="Too many requests"
        )

    # Save request time
    request_history[client_ip].append(current_time)