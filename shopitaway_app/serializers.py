from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.Serializer):
	name = serializers.CharField(max_length = 100)
	email = serializers.EmailField()
	password = serializers.CharField(min_length = 8)

class LoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField(min_length = 8)

class itemTypeSerializer(serializers.Serializer):
	itype = serializers.CharField(max_length=50)
