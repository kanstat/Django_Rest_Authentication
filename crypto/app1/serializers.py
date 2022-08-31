
from tkinter.ttk import Style
from xml.dom import ValidationErr
from rest_framework import serializers
from app1.models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django .utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class UserRegistrationSerializer(serializers.ModelSerializer):
    # we are writing this because we need confirm password field in our registration
    # request
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}}


# validating password and confirm password while registration


    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password Does not Match")
        return data

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['email', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']


class UserChangePassword(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'password2']

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password Does not Match")
        user.set_password(password)
        user.save()
        return super().validate(data)


class SendPasswordResetToEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email']

    def validate(self, data):
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            print(user.id)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print("user id", uid)
            token = PasswordResetTokenGenerator().make_token(user=user)
            print("token", token)
            link = 'http://127.0.0.1:8000/api/user/resetpassword/'+uid+'/'+token
            print("link", link)
            return data
        else:
            raise ValidationErr("You are not registred user")


class UserPasswordResetSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'password2']

    def validate(self, data):
        try:
            password = data.get('password')
            password2 = data.get('password2')
            user_id = self.context.get('user_id')
            print('idddddddddddddd', user_id)
            token = data.get('token')
            if password != password2:
                raise serializers.ValidationError("Password Does not Match")
            id = smart_str(urlsafe_base64_decode(user_id))
            print(id)
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationErr('Token is not valid or expired')
            user.set_password(password)
            user.save()
            return data
        # provide extra security if manupulation in token
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user=user, token=token)
            raise ValidationErr('Token is not valid or expired')
