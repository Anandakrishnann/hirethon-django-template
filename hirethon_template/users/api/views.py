from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from dj_rest_auth.views import LoginView
from dj_rest_auth.serializers import LoginSerializer

from .serializers import UserSerializer, LoginResponseSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "pk"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user, context={"request": request})
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        elif request.method == 'PATCH':
            serializer = UserSerializer(request.user, data=request.data, partial=True, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK, data=serializer.data)
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class CustomLoginView(LoginView):
    """Custom login view that returns user details with refresh token"""
    
    def post(self, request, *args, **kwargs):
        # Use the parent login logic (this will set httpOnly access token cookie automatically)
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            # Get user from the response data
            user_data = response.data.get('user', {})
            user_id = user_data.get('pk')
            
            if user_id:
                # Get the actual user object
                user = User.objects.get(pk=user_id)
                
                # Generate refresh token to return in response body
                refresh = RefreshToken.for_user(user)
                refresh_token = str(refresh)
                
                # Create response data with user details and refresh token
                user_serializer = UserSerializer(user, context={"request": request})
                
                response_data = {
                    "user": user_serializer.data,
                    "refresh": refresh_token,
                    "message": "Login successful"
                }
                
                # Create response with data
                response_obj = Response(response_data, status=status.HTTP_200_OK)
                
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


