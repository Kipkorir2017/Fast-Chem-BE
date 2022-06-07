from rest_framework import serializers
from .models import Profile,Pharmacy
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email']
    
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Profile
        fields = ['id','user','name', 'profile_pic','location', 'contact']

class PharmacySerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Pharmacy
        fields = [ 'name', 'location', 'medicine', 'price','description']