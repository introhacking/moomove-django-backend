# middleware.py
import json
import time
from .models import *
from django.http import JsonResponse

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

# class ClientAccessMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
        
#     # [ 18/FEB/25 ]
#     def __call__(self, request):
#         if request.user.is_authenticated:
#             if not request.user.is_admin and not request.user.is_superuser:
#                 if not request.user.client:
#                     return JsonResponse({"error": "Access Denied: No client assigned"}, status=403)
#         return self.get_response(request)    

    # def __call__(self, request):
    #     # Check if the user is authenticated and linked to a client
    #     if request.user.is_authenticated and not request.user.client:
    #         return JsonResponse({'error': 'Access Denied: No client assigned'}, status=403)
    #     return self.get_response(request)    



# [ 11/03/2025]

class ClientAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # For non-admin users, enforce that a client is assigned.
            if not (request.user.is_admin or request.user.is_superuser):
                if not request.user.client:
                    return JsonResponse({"error": "Access Denied: No client assigned"}, status=403)

            # Attach an active client context to the request.
            # For admin users, use current_client if set; otherwise, it remains None.
            # For regular users, use the assigned client.
            if request.user.is_admin or request.user.is_superuser:
                request.active_client = request.user.current_client  # May be None if not switched.
            else:
                request.active_client = request.user.client

        return self.get_response(request)
