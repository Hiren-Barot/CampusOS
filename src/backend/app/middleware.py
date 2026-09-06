import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import uuid

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        request_id = str(uuid.uuid4())[:8]
        
        logger.info(f"[{request_id}] {request.method} {request.url.path}")
        
        start_time = time.time()
        
        response = await call_next(request)
        
        duration = (time.time() - start_time) * 1000 
        
        logger.info(
            f"[{request_id}] {request.method} {request.url.path} → "
            f"{response.status_code} ({duration:.2f}ms)"
        )
        
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time"] = f"{duration:.2f}ms"
        
        return response