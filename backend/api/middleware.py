import time
import logging

logger = logging.getLogger(__name__)

class APIMetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = round((time.time() - start_time) * 1000, 2)

        user = getattr(request, "user", None)
        username = user.username if user and user.is_authenticated else "Anonymous"

        logger.info(
            f"[API METRIC] {request.method} {request.path} by {username} - "
            f"Status: {response.status_code} - Time: {duration}ms"
        )

        return response