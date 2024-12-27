# middleware.py
import json
import time
from .models import AuditLog

class AuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time

        if request.user.is_authenticated:
            try:
                AuditLog.objects.create(
                    user=request.user,
                    method=request.method,
                    path=request.get_full_path(),
                    query_params=json.dumps(request.GET.dict()),
                    body=request.body.decode('utf-8') if request.body else '',
                    status_code=response.status_code,
                    duration=duration
                )
            except Exception as e:
                # Handle exceptions during logging gracefully
                print(f"Error creating audit log: {str(e)}")

        return response