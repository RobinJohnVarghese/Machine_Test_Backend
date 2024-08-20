from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import  logout
from .models import UserAccount
from .serializers import UserAccountSerializer, SignupSerializer, LoginSerializer
# from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model, authenticate
from django.http import JsonResponse
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'user': UserAccountSerializer(user).data,
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Check if the user is active
            if not user.is_active:
                raise AuthenticationFailed("User account is inactive.")

            # Handle login success (e.g., generate token, etc.)
            # return Response({"message": "Login successful","user":user}, status=status.HTTP_200_OK)
            refresh = RefreshToken.for_user(user)
            response = JsonResponse({
                    "message": "Login successful",
                    "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    },
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "name": user.name,
                        "email": user.email,
                        "mobile": user.mobile,
                    }
                })
            response.data = {"Success" : "Login successfully","data":user}
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
