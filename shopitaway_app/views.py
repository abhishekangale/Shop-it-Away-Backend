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

import random



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
				data['OTP'] = ""
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
				return Response({"message": "Success", "uid": uid, "name": data_ref['name'], "buyitems": data_ref['buyitems'], "wishlist": data_ref['wishlist']}, status = status.HTTP_200_OK)
			else:
				return Response({"message": "Invalid Password"}, status = status.HTTP_401_UNAUTHORIZED)

		# user not found
		except Exception as e:
			return Response({"message": "Invalid email"}, status = status.HTTP_401_UNAUTHORIZED)

	return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def item(request):

	serializer = itemTypeSerializer(data = request.data)

	if serializer.is_valid():
		itemtype = serializer.data['itype']

		try:
			dataref = db.collection(u'items').where(u'type',u'==',itemtype).get()
			idlist = []
			for i in dataref:
				idlist.append(i.id)
			
			itemsinfo = []
			for i in idlist:
				datadict = db.collection(u'items').document(i).get().to_dict()
				itemsinfo.append(datadict)
			
			return Response({"message": "Success", "list": itemsinfo}, status = status.HTTP_200_OK)

		except Exception as e:
			return Response({"message": "Invalid type"}, status = status.HTTP_401_UNAUTHORIZED)

	return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def itemcount(request):
	try:
		dataref = db.collection(u'items').get()
		idlist = []
		for i in dataref:
			idlist.append(i.id)
		
		itemsinfo = []
		for i in idlist:
			datadict = db.collection(u'items').document(i).get().to_dict()
			itemsinfo.append(datadict)
		
		itemssort = sorted(itemsinfo, key = lambda i: i['buycount'],reverse=True)
		print(itemssort)
		return Response({"message": "Success", "list": itemssort}, status = status.HTTP_200_OK)

	except Exception as e:
		return Response({"message": "Invalid type"}, status = status.HTTP_401_UNAUTHORIZED)

# @api_view(['GET'])
# def otp(request):
# 	otp = random.randrange(1000,9999)
@api_view(['POST'])
def item(request):

	serializer = itemTypeSerializer(data = request.data)

	if serializer.is_valid():
		itemtype = serializer.data['itype']

		try:
			dataref = db.collection(u'items').where(u'type',u'==',itemtype).get()
			idlist = []
			for i in dataref:
				idlist.append(i.id)
			
			itemsinfo = []
			for i in idlist:
				datadict = db.collection(u'items').document(i).get().to_dict()
				itemsinfo.append(datadict)
			
			return Response({"message": "Success", "list": itemsinfo}, status = status.HTTP_200_OK)

		except Exception as e:
			return Response({"message": "Invalid type"}, status = status.HTTP_401_UNAUTHORIZED)

	return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def postitem(request):

	serializer = postitemSerializer(data = request.data)

	if serializer.is_valid():
		item = {
				"buycount": serializer.data['buycount'],
				"description": serializer.data['description'],
				"name": serializer.data['name'],
				"type": serializer.data['type'],
				"image": serializer.data['image'],
				"stock": serializer.data['stock'],
				"price": serializer.data['price']
			}
		try:
			db.collection(u'items').add(item)
			
			return Response({"message": "Success"}, status = status.HTTP_200_OK)

		except Exception as e:
			return Response({"message": "Invalid type"}, status = status.HTTP_401_UNAUTHORIZED)

	return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def updateitem(request):

	serializer = updateitemSerializer(data = request.data)

	if serializer.is_valid():
		item = {
				"id": serializer.data['id'],
				"name": serializer.data['name'],
				"description": serializer.data['description'],
				"stock": serializer.data['stock'],
				"price": serializer.data['price']
			}
		try:
			db.collection(u'items').document(item["id"]).update({
				u'name' : item["name"],
				u'description' : item["description"],
				u'stock' : item["stock"],
				u'price' : item["price"]
				}
			)

			return Response({"message": "Success"}, status = status.HTTP_200_OK)

		except Exception as e:
			return Response({"message": "Invalid type"}, status = status.HTTP_401_UNAUTHORIZED)

	return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def deleteitem(request):

	serializer = idSerializer(data = request.data)

	if serializer.is_valid():
		try:
			db.collection(u'items').document(serializer.data['id']).delete()

			return Response({"message": "Success"}, status = status.HTTP_200_OK)

		except Exception as e:
			return Response({"message": "Invalid type"}, status = status.HTTP_401_UNAUTHORIZED)

	return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def assignOTP(request):

	serializer = idSerializer(data = request.data)

	if serializer.is_valid():
		try:
			otp = random.randint(100000,999999)
			otp = str(otp)
			db.collection(u'users').document(serializer.data['id']).update({
				u'OTP' : otp
			})

			return Response({"message": "Success"}, status = status.HTTP_200_OK)

		except Exception as e:
			return Response({"message": "Invalid type"}, status = status.HTTP_401_UNAUTHORIZED)

	return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def verifyOTP(request):
	serializer = otpSerializer(data = request.data)
	if serializer.is_valid():
		try:
			user = db.collection(u'users').document(serializer.data['id']).get().to_dict()
			print(user['OTP'])
			print(serializer.data['otp'])
			if str(user['OTP'])!= str(serializer.data['otp']) :
				return Response({"message": "Incorrect OTP"}, status = status.HTTP_200_OK)
			else :
				return Response({"message": "OTP Successfully verified"}, status = status.HTTP_200_OK)


		except Exception as e:
			return Response({"message": "Invalid type"}, status = status.HTTP_401_UNAUTHORIZED)

	return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
