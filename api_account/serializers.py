from rest_framework import serializers, exceptions
from django.contrib.auth import authenticate
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'email', 'first_name', 'last_name',
                  'role', 'birth_date', 'last_login', 'date_joined', 'is_active','image']
        read_only_fields = ('date_joined', 'last_login')


class DeleteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'email', 'first_name', 'last_name',
                  'role', 'birth_date', 'last_login', 'date_joined', 'is_active','image']
        read_only_fields = ('date_joined', 'last_login', 'email', 'first_name',
                            'last_name', 'role', 'birth_date', 'is_active')


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name',
                  'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Passwords must match'})
        user.set_password(password)
        user.role = 1
        user.save()
        return user


class LoginVisitorSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email', '')
        password = data.get('password', '')

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if user.is_active:
                    if user.role == 1:
                        data['user'] = user
                    else:
                        msg = "this user is not visitor"
                        raise exceptions.ValidationError(msg)
                else:
                    msg = "this user has been blocked"
                    raise exceptions.ValidationError(msg)

            else:
                msg = "user doesn't exist"
                raise exceptions.ValidationError(msg)
        else:
            msg = "must provide an email and a password"
            raise exceptions.ValidationError(msg)
        print("data : ", data, " / ")
        return data


class LoginStaffSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email', '')
        password = data.get('password', '')

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if user.is_active:
                    if user.is_staff:
                        data['user'] = user
                    else:
                        msg = "this user is not staff"
                        raise exceptions.ValidationError(msg)
                else:
                    msg = "this user has been blocked"
                    raise exceptions.ValidationError(msg)

            else:
                msg = "user doesn't exist"
                raise exceptions.ValidationError(msg)
        else:
            msg = "must provide an email and a password"
            raise exceptions.ValidationError(msg)
        print("data : ", data, " / ")
        return data


class AddUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'first_name', 'last_name',
                           'role', 'birth_date', 'is_active', ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            role=self.validated_data['role'],
            birth_date=self.validated_data['birth_date'],
            is_active=self.validated_data['is_active'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if self.validated_data['role'] != 1:
            user.is_staff = True

        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Passwords must match'})
        user.set_password(password)
        user.save()
        return user

class SocialSerializer(serializers.Serializer):
    """
    Serializer which accepts an OAuth2 access token.
    """
    access_token = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
    )
