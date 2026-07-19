import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logger import logger





class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        

        # Get existing request ID or generate a new one
        request_id = request.headers.get("X-Request-ID")

        if not request_id:
            request_id = str(uuid.uuid4())

        # Start timer
        start_time = time.perf_counter()

        # Process request
        response = await call_next(request)

        # Calculate duration
        end_time = time.perf_counter()

        duration_ms = round(
            (end_time - start_time) * 1000,
            2
        )

        # Add request ID to response header
        response.headers["X-Request-ID"] = request_id

        # Create log
        logger.info(
    {
        "request_id": request_id,
        "method": request.method,
        "path": request.url.path,
        "status": response.status_code,
        "duration_ms": duration_ms
    },
    extra={"request_id": request_id}
)
        return response