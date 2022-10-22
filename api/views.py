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

class CompleteProfileView(APIView):
    def post(self, request, format=None):
        username = request.data.get('username')
        fullname = request.data.get('fullname')
        college = request.data.get('college')
        skills = request.data.get('skills')
        field = request.data.get('field')
        linkedin = request.data.get('linkedin')
        github = request.data.get('github')
        instagram = request.data.get('instagram')

        # Creating new user
        user = User.objects.filter(username=username).first()
        profile = Profile.objects.get(user=user)
        # Creating profile page
        profile.full_name = fullname
        profile.college = college
        profile.field = field
        profile.skills = skills
        profile.linkedin = linkedin
        profile.instagram = instagram
        profile.github = github
        profile.save(update_fields=["college", "field", "skills", "linkedin", "instagram", "github", "full_name"])

        #registration_mail(email, data)
        return Response({"Message": "Done !"}, status=status.HTTP_200_OK)

class GetUserData(APIView):
    lookup_url_kwarg = "username"
    def post(self, request, format=None):
        username = request.data.get(self.lookup_url_kwarg)
        user = User.objects.filter(username=username).first()  
        profile = Profile.objects.get(user=user) 
        completed = len(profile.full_name)>0
        payload = {
            "emailid": user.email,
            "contact": profile.mobile,
            "linkedin": profile.linkedin,
            "instagram": profile.instagram,
            "github": profile.github,
            "enrolled": CTOHuntProgress.objects.filter(user=user).exists(),
            "completed": completed
        }
        return Response(payload, status=status.HTTP_200_OK)
        
        