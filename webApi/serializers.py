import re
from rest_framework import serializers
from passlib.hash import django_pbkdf2_sha256 as handler
from .models import *

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["fname", "lname", "email", "password", "profile"]
    
    def validate(self, attrs):
        if len(attrs['password']) < 8 :
            raise serializers.ValidationError("Password Length must be greaterthan 8")
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_status = re.match(pattern, attrs['email'])
        if not email_status:
            raise serializers.ValidationError("Email pattern is not valid")
        return attrs
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['password'] = handler.hash(password)
        return super().create(validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password"]

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        fetch_user = User.objects.filter(email=email).first()
        if not fetch_user:
            raise serializers.ValidationError("Email not found . . .")
        check_pass = handler.verify(password, fetch_user.password)
        if not check_pass:
            raise serializers.ValidationError("Wrong Password !!!")
        attrs["fetch_user"] = fetch_user
        return attrs


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class ChatsSerializer(serializers.ModelSerializer):
    class Meta:
        model= Chats
        fields= '__all__'


class GetMessageSerializer(serializers.ModelSerializer):
    user_fullname = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format= "%d-%m-%Y %H:%M:%S")
    chatname= serializers.CharField(source= "chatid.chat_name")
    user_id= serializers.CharField(source= 'user.id')

    def get_user_fullname(self, obj):
        return f"{obj.user.fname} {obj.user.lname}"

    class Meta:
        model = Message
        fields = ['id', 'user_fullname', 'user_id', 'chatname', 'chatid', 'message', 'created_at']
