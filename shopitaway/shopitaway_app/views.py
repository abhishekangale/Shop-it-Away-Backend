from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.hashers import make_password, check_password

from .serializers import *

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response




from .connect import getDBConnection


db= getDBConnection()


@api_view(['POST'])
def register(request):
	"""
	Register new user
	{
		"name": "XYZ",
		"email": "abcd@gmail.com",
		"password": "password"
	}
	"""
	serializer = UserSerializer(data = request.data)

	if serializer.is_valid():
		data = serializer.data

		# check if user already registered
		try:
			user_ref = db.collection(u'users').where(u'email', u'==', data["email"])
			uid = user_ref.get()[0].id
			return Response({"message": "Email already registered"}, status = status.HTTP_400_BAD_REQUEST)
		# if new user
		except:
			# successfully added to db
			try:
				# hash the password
				data["password"] = make_password(data['password'])
				# add to database
				user = db.collection(u'users').add(data)
				return Response({"message": "User registered successfully"}, status = status.HTTP_201_CREATED)

			# error in adding to db
			except:
				return Response("Check logs", status = status.HTTP_400_BAD_REQUEST)

	return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
	"""
	Login User
	{
		"email": "abcd@gmail.com",
		"password": "password"
	}
	"""
	serializer = LoginSerializer(data = request.data)

	if serializer.is_valid():
		email = serializer.data['email']
		password = serializer.data['password']

		# search for user
		try:
			user_ref = db.collection(u'users').where(u'email', u'==', email).get()[0]
			uid = user_ref.id

			# verify password
			user_pwd = user_ref.to_dict()['password']
			if check_password(password, user_pwd):
				data_ref = db.collection(u'users').document(uid).get().to_dict()
				return Response({"message": "Success", "uid": uid, "name": data_ref['name']}, status = status.HTTP_200_OK)
			else:
				return Response({"message": "Invalid Password"}, status = status.HTTP_401_UNAUTHORIZED)

		# user not found
		except Exception as e:
			return Response({"message": "Invalid email"}, status = status.HTTP_401_UNAUTHORIZED)

	return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
