from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework import status
from rest_framework.response import Response


class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication that supports both Authorization header and cookies
    Returns 401 instead of 403 for invalid tokens
    """
    
    def authenticate(self, request):
        # First try to get token from Authorization header
        header = self.get_header(request)
        if header is not None:
            raw_token = self.get_raw_token(header)
            if raw_token is not None:
                try:
                    validated_token = self.get_validated_token(raw_token)
                    return self.get_user(validated_token), validated_token
                except (InvalidToken, TokenError):
                    # Continue to try cookie authentication
                    pass
        
        # If no header token, try to get token from cookies
        cookie_token = request.COOKIES.get('access_token')
        if cookie_token:
            try:
                validated_token = self.get_validated_token(cookie_token)
                return self.get_user(validated_token), validated_token
            except (InvalidToken, TokenError):
                # Return None to let DRF handle it with 401
                return None
        
        return None


def custom_authentication_handler(exc, context):
    """
    Custom exception handler to return 401 for authentication errors
    """
    from rest_framework.views import exception_handler
    
    response = exception_handler(exc, context)
    
    if response is not None:
        # Check if it's an authentication error
        if hasattr(exc, 'detail') and 'Authentication credentials were not provided' in str(exc.detail):
            response.status_code = status.HTTP_401_UNAUTHORIZED
        elif hasattr(exc, 'detail') and 'Given token not valid' in str(exc.detail):
            response.status_code = status.HTTP_401_UNAUTHORIZED
        elif response.status_code == 403 and 'Authentication' in str(exc):
            response.status_code = status.HTTP_401_UNAUTHORIZED
    
    return response
