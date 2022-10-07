from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class ProfileSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()
    def split_skills(self, obj):
        return [ skill for skill in self.skills.split(',') ]
    class Meta:
        model = Profile
        fields = ('user', 'slug', 'skills,', 'points')

class CTOHuntProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CTOHuntProgress
        exclude = ('id', 'max_round_cleared', 'user')
