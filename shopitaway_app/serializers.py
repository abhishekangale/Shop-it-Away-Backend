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

class postitemSerializer(serializers.Serializer):
	buycount = serializers.IntegerField()
	description = serializers.CharField(max_length=200)
	image = serializers.CharField(max_length=200)
	name = serializers.CharField(max_length=200)
	stock = serializers.IntegerField()
	type = serializers.CharField(max_length=200)
	price = serializers.IntegerField()

class updateitemSerializer(serializers.Serializer):
	id = serializers.CharField()
	description = serializers.CharField(max_length=200)
	name = serializers.CharField(max_length=200)
	stock = serializers.IntegerField()
	price = serializers.IntegerField()

class idSerializer(serializers.Serializer):
	id = serializers.CharField()

class otpSerializer(serializers.Serializer):
	id = serializers.CharField()
	otp = serializers.CharField()

