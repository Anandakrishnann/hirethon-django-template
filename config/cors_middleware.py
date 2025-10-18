from django.utils.deprecation import MiddlewareMixin


class CustomCorsMiddleware(MiddlewareMixin):
    """
    Custom CORS middleware to ensure CORS headers are added
    """
    
    def process_response(self, request, response):
        # Add CORS headers to all responses
        origin = request.META.get('HTTP_ORIGIN')
        
        # Allow requests from frontend origins
        allowed_origins = [
            'http://localhost:3000',
            'http://localhost:3001', 
            'http://localhost:5173',
            'http://localhost:8080',
            'http://127.0.0.1:3000',
            'http://127.0.0.1:3001',
            'http://127.0.0.1:5173',
            'http://127.0.0.1:8080',
        ]
        
        if origin and origin in allowed_origins:
            response['Access-Control-Allow-Origin'] = origin
            response['Access-Control-Allow-Credentials'] = 'true'
            response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH'
            response['Access-Control-Allow-Headers'] = 'accept, accept-encoding, authorization, content-type, dnt, origin, user-agent, x-csrftoken, x-requested-with'
            response['Access-Control-Max-Age'] = '86400'
        
        # Handle preflight requests
        if request.method == 'OPTIONS':
            response.status_code = 200
            
        return response
