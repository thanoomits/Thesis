from rest_framework import serializers
from .models import User, Profile, MyCourse, Lessons


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']
        

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class LessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        fields = '__all__'

class MyCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyCourse
        fields = '__all__'