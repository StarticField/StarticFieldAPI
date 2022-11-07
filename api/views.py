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
import datetime
from .mails import *
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
        return Response(serializer.errors, status=status.HTTP_200_OK)

class CompleteProfileView(APIView):
    def post(self, request, format=None):
        username = request.data.get('username')
        fullname = request.data.get('fullname')
        college = request.data.get('collegename')
        skills = request.data.get('skills')
        field = request.data.get('field')
        linkedin = request.data.get('linkedin')
        github = request.data.get('github')
        instagram = request.data.get('instagram')
        print("username ::::: ", username)
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
        profile.completed = True
        profile.save(update_fields=["college", "field", "skills", "linkedin", "instagram", "github", "full_name", "completed"])

        #registration_mail(email, data)
        return Response({"Message": "Done !"}, status=status.HTTP_200_OK)

class GetUserData(APIView):
    lookup_url_kwarg = "username"
    def get(self, request, format=None):
        username = request.GET.get("username")
        print("username >>>> ", username)
        user = User.objects.filter(username=username).first()  
        profile = Profile.objects.get(user=user) 
        payload = {
            "fullname": profile.full_name,
            "emailid": user.email,
            "contact": profile.mobile,
            "linkedin": profile.linkedin,
            "instagram": profile.instagram,
            "github": profile.github,
            "enrolled": CTOHuntProgress.objects.filter(user=user).exists(),
            "completed": profile.completed
        }
        return Response(payload, status=status.HTTP_200_OK)
        
class GetEnrolledStatus(APIView):
    def get(self, request, format=None):
        username = request.GET.get("username")
        user = User.objects.filter(username=username).first()  
        profile = Profile.objects.get(user=user) 
        if CTOHuntProgress.objects.filter(user=user).exists():
            cto_status = "enrolled"
        else :
            if profile.completed:
                cto_status = "available"
            else :
                cto_status = "unavailable"
        if MockPitchProgress.objects.filter(user=user).exists():
            mock_status = "enrolled"
        else :
            mock_status = "available"
        payload = {
            "ctohunt": cto_status,
            "mockpitch": mock_status,
        }
        return Response(payload, status=status.HTTP_200_OK)

class GetFormAvailableView(APIView):
    def get(self, request, name):
        username = request.GET.get("username")
        user = User.objects.filter(username=username).first()
        available = False
        if name=="mockpitch":
            query = MockPitchProgress.objects.filter(user=user)
            if query.exists():
                available = True
            return Response({"available": available}, status=status.HTTP_200_OK)
        """elif name=="ctohunt":
            query = CTOHuntProgress.objects.filter(user=user)
            if query.exists():
                available = False
            return Response({"available": available}, status=status.HTTP_200_OK)"""
        return Response({"error": "Some error"}, status=status.HTTP_204_NO_CONTENT)

class EnrollInEvent(APIView):
    def post(self, request, format=None):
        username = request.data.get("username")
        name = request.data.get("event")
        user = User.objects.filter(username=username).first()
        if name=="mockpitch":
            MockPitchProgress.objects.create(user=user)
            return Response({"enrolled": "available"}, status=status.HTTP_200_OK)
        elif name=="ctohunt":
            CTOHuntProgress.objects.create(user=user)
            return Response({"enrolled": "available"}, status=status.HTTP_200_OK)
        return Response({"error": "Some error"}, status=status.HTTP_204_NO_CONTENT)

class ResetKeyVerifyView(APIView):
    def get(self, request, format=None):
        email = request.GET.get("email")
        user = User.objects.filter(email=email)
        if user.exists():
            user = user.first()
            send_reset_mail(email, user.username)
            return Response({"message": "sent"}, status=status.HTTP_200_OK)
        return Response({"message": "error"}, status=status.HTTP_204_NO_CONTENT)

    def post(self, request, format=None):
        username = request.data.get("username")
        password = request.data.get("password")
        key = request.data.get("key")
        # password reset
        user = User.objects.get(username=username)
        user.set_psswd(password)
        user.save(update_fields=["password"])
        # delete instance
        inst = PasswordResetRequest.objects.filter(username=username, key=key)
        inst.delete()
        return Response({"message": "Done"}, status=status.HTTP_200_OK) 

class ResetKeyVerifyView(APIView):
    def post(self, request, format=None):
        username = request.data.get("username")
        key = request.data.get("key")
        inst = PasswordResetRequest.objects.filter(username=username, key=key)
        if inst.exists():
            inst = inst.first()
            if inst.expire_in>datetime.datetime.now():
                return Response({"valid": True}, status=status.HTTP_200_OK)
            return Response({"valid": False}, status=status.HTTP_200_OK)
        return Response({"valid": False}, status=status.HTTP_200_OK)
