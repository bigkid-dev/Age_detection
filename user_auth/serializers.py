from rest_framework import serializers
from .models import CustomUser as User
from rest_framework_simplejwt.tokens import RefreshToken
import signing
from typing import Any


class SignupSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'phone_number', 'name')

    def authenticate_user(self, user: User):
        refresh_token = RefreshToken.for_user(user)
        self.token = {
            "backend": str(refresh_token.access_token)
        }

    def create(self, validated_data):
        user = super().create(validated_data)
        password = validated_data["password"]
        user.set_password(password)
        user.is_active = True
        user.save()
        self.authenticate_user(user)
        return user        

    
    def validate(self, attrs):
        error = {}
        if not attrs.get("username"):
            error["errors"] = "username field is required"
            raise serializers.ValidationError(error)
        
        if not attrs.get("password"):
            error["errors"] = "password field is required"
            raise serializers.ValidationError(error)
        
        if not attrs.get("phone_number"):
            error["errors"] = "phone number field is required"
            raise serializers.ValidationError(error)
        
        username = attrs.get("username")
        password = attrs.get("password")
        phone_number = attrs.get("phone_number")

        if User.objects.filter(username=username).exists():
            error["errors"] = "username already exists"
            raise serializers.ValidationError(error)
        
        if User.objects.filter(phone_number=phone_number).exists():
            error["errors"] = "phone number already exists"
            raise serializers.ValidationError(error)


        return super().validate(attrs)
    
    def to_representation(self, instance: User):
       
        data = {**super().to_representation(instance)}
        if self.token:
            data.update({"auth_token": self.token})
        return data
    
    
class LoginSerializers(serializers.ModelSerializer):

    email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password')

    
    def validate(self, attrs):
        error = {}
        email = attrs.get("email")
        password = attrs.get("password")


        if not User.objects.filter(email=email).exists():
            error["error"] = "This user does not exist"
            raise serializers.ValidationError(error)
        
        user = User.objects.filter(email=email).first()
        if not user.password == password:
            error["error"] = "Invalid Credentials"
            raise serializers.ValidationError(error)         

        self.authenticate_user(user)
        
        return user


    def to_representation(self, instance):
        data = {** super().to_representation(instance)}
        if  self.token:
            data.update({"auth_token": self.token})


    def authenticate_user(self, user):
        refresh_token = RefreshToken.for_user(user)
        self.token = {
            "backend": str(refresh_token.access_token)
        }
    


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    password_reset_key = serializers.CharField(write_only=True)

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        super().validate(attrs)

        # unsign password_reset_key
        try:
            signer = signing.TimestampSigner()
            data = signer.unsign_object(attrs["password_reset_key"])
            user = User.objects.filter(
                email=attrs["email"], password_reset_key=data["key"]
            ).first()
        except KeyError as error:
            print(error)
        else:
            if user:
                user.password_reset_key = None
                user.set_password(attrs["new_password"])
                user.save(update_fields=["password", "password_reset_key"])
                return {}
        raise serializers.ValidationError(
            "An error occured in the process please retry."
        )
