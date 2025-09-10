from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

User = get_user_model()


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]  # Anyone can register

    def post(self, request):
        context = {"success": 0, "message": "Something went wrong"}
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                context["success"] = 1
                context["message"] = "User registered successfully"
                context["data"] = UserSerializer(user).data
                return Response(context, status=status.HTTP_201_CREATED)
            else:
                context["message"] = serializer.errors
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            context["message"] = str(e)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]  # Login is public

    def post(self, request):
        context = {"success": 0, "message": "Invalid credentials"}
        try:
            email = request.data.get("email")
            password = request.data.get("password")

            if not email or not password:
                context["message"] = "Email and password are required"
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            user = authenticate(request, email=email, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                context["success"] = 1
                context["message"] = "Login successful"
                context["data"] = {
                    "user": UserSerializer(user).data,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "email" : user.email,
                    "role" : user.role,
                }
                return Response(context, status=status.HTTP_200_OK)
            else:
                return Response(context, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            context["message"] = str(e)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Only logged-in users can logout

    def post(self, request):
        context = {"success": 0, "message": "Something went wrong"}
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                context["message"] = "Refresh token is required"
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()  # Requires blacklist app enabled
            context["success"] = 1
            context["message"] = "Logout successful"
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context["message"] = str(e)
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

