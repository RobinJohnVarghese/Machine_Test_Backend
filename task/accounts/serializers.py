from rest_framework import serializers
from .models import UserAccount
from .validator import CustomPasswordValidator
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.core.exceptions import ValidationError



class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('id', 'name', 'email', 'mobile', 'username', 'is_active', 'is_staff', 'is_superuser')

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserAccount
        fields = ('name', 'email', 'mobile', 'username', 'password')
        
    def validate_username(self, value):
        if UserAccount.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    def validate_password(self, value):
        # Apply custom password validation
        validator = CustomPasswordValidator()
        try:
            validator.validate(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):
        user = UserAccount.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            mobile=validated_data['mobile']
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError("Both 'username' and 'password' are required.")

        # Check if the username exists
        try:
            user = UserAccount.objects.get(username=username)
        except UserAccount.DoesNotExist:
            raise AuthenticationFailed("Invalid username.")

        # Check if the password is correct
        if not user.check_password(password):
            raise AuthenticationFailed("Invalid password.")

        # Return user if validation is successful
        return {
            'user': user
        }

