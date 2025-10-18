from dj_rest_auth.registration.views import RegisterView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .api.serializers import UserSerializer
from .registration_serializer import CustomRegisterSerializer

User = get_user_model()


class CustomRegistrationView(RegisterView):
    """Custom registration view that handles the name field"""
    serializer_class = CustomRegisterSerializer
    
    def create(self, request, *args, **kwargs):
        """Override create to return user details with refresh token"""
        response = super().create(request, *args, **kwargs)
        
        if response.status_code == 201:
            # Get the created user
            user_data = response.data.get('user', {})
            user_id = user_data.get('pk')
            
            if user_id:
                # Get the actual user object with name field
                user = User.objects.get(pk=user_id)
                
                # Create response data with user details including name
                user_serializer = UserSerializer(user, context={"request": request})
                
                response_data = {
                    "user": user_serializer.data,
                    "refresh": response.data.get('refresh')
                }
                
                # Create response with data
                response_obj = Response(response_data, status=status.HTTP_201_CREATED)
                
                # Copy cookies from parent response (access token will be httpOnly)
                if hasattr(response, 'cookies'):
                    for cookie in response.cookies.values():
                        response_obj.set_cookie(
                            key=cookie.key,
                            value=cookie.value,
                            max_age=cookie.get('max-age'),
                            expires=cookie.get('expires'),
                            path=cookie.get('path', '/'),
                            domain=cookie.get('domain'),
                            secure=cookie.get('secure', False),
                            httponly=cookie.get('httponly', True),
                            samesite=cookie.get('samesite', 'Lax')
                        )
                
                return response_obj
        
        return response
