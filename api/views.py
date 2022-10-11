from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status, permissions
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
import random
import requests
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
import json
# Create your views here.

class UserRegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    lookup_url_kwarg = "contact"

    def post(self, request, format='json'):
        contact = request.data.get(self.lookup_url_kwarg)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                profile = Profile.objects.create(
                    user=user,
                    mobile=contact
                )
                #registration_mail(email, data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CTOHuntRegistrationView(APIView):
    def post(self, request, format=None):
        data = request.POST
        username = data['username']
        email = data['email']
        college = data['college']
        skills = data['skills']
        pursuing = data['pursuing']
        field = data['field']
        linkedin = ""
        github = ""
        if 'linkedin' in data:
            linkedin = data['linkedin']
        if 'github' in data:
            github = data['github']
        # Creating new user
        random_psswd = generate_code()
        user = User.objects.create(username=username, email=email)
        user.set_password(random_psswd)
        # Creating profile page
        profile = Profile.objects.create(
            user=user,
            college=college,
            skills=skills,
            pursuing=pursuing,
            field=field,
            linkedin=linkedin,
            github=github,
        )
        registration_mail(email, data)
        return Response({"Message": "Done !"}, status=status.HTTP_200_OK)

class GetUserData(APIView):
    lookup_url_kwarg = "username"
    def post(self, request, format=None):
        username = request.data.get(self.lookup_url_kwarg)
        user = User.objects.filter(username=username).first()  
        profile = Profile.objects.get(user=user) 
        payload = {
            "emailid": user.email,
            "contact": profile.mobile,
            "linkedin": profile.linkedin,
            "instagram": profile.instagram,
            "enrolled": CTOHuntProgress.objects.filter(user=user).exists()
        }
        return Response(payload, status=status.HTTP_200_OK)
        
        