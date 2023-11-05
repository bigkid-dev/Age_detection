from django.shortcuts import render
from .serializers import *
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser, ResetPasswordOTP
from rest_framework import status as http_status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.request import Request
from rest_framework import permissions
from rest_framework import status
from rest_framework import generics

# Create your views here.

class SignUpAPIView(CreateAPIView):
    serializer_class = SignupSerializers
    

# class LoginAPIView(CreateAPIView):
#     serializer_class = LoginSerializers
    


class LoginAPIView(APIView):
    
    def post(self, request, format=None):
        try:
            email = request.data["email"]
            password = request.data["password"]
            error = {}

            if not User.objects.filter(email=email).exists():
                error["error"] = "user with email do not exist"
                return Response(error, status=http_status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.filter(email=email).first()
            if not user.check_password(str(password)):
                error["error"] = "wrong Password"
                return Response(error, status=http_status.HTTP_400_BAD_REQUEST)
            
            refresh_token = RefreshToken.for_user(user)
            auth_token = {
                "backend": str(refresh_token.access_token)
            }
            return Response(auth_token, status=http_status.HTTP_200_OK)
        
        except Exception as e:
            auth_token = {
                "backend": str(e)
            }
            
            return Response(auth_token, status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)

        

class  ResetPassword(APIView):

    def post(self, request, format=None):
        error = {}
        email = request.data["email"]
        password_one = request.data["password1"]
        password_two =  request.data["password2"]

        if not (str(password_one) == str(password_two)):
            error["errors"] = "password are not the same"
            return Response(error, status=400)
        
        if not CustomUser.objects.filter(email=email).exists():
            error["errors"] = "This email does not exist"
            return Response(error, status=400) 
        
        user =  CustomUser.objects.filter(email=email).first()
        user.set_password(password_one)
        user.save()
        return Response({"backend": "password Changed successfully"}, status=201)
    



# class GetResetPasswordOTPAPIView(generics.GenericAPIView):
#     serializer_class = OTPCreationSerializer
#     permission_classes = [permissions.AllowAny]

#     def post(self, request: Request) -> Response:
#         """Generate otp for password reset and send to users email."""

#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = User.objects.filter(email=serializer.validated_data["email"]).first()

#         if user:
#             otp, signed_pin = generate_otp_pin(user)

#             # delete all active otp pins
#             old_pins = ResetPasswordOTP.objects.filter(user=user, is_active=True)

#             for pin in old_pins:
#                 pin.is_active = False
#                 pin.is_expired = True

#             ResetPasswordOTP.objects.bulk_update(
#                 old_pins, fields=["is_active", "is_expired"]
#             )

#             # create new otp pin entry
#             ResetPasswordOTP.objects.create(user=user, signed_pin=signed_pin)

#             # send otp to user's email
       

#         return Response(status=status.HTTP_200_OK)

