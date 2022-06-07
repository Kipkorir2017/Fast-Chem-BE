from django.shortcuts import render
from rest_framework import serializers
from rest_framework .response import Response
from .models import Profile, Pharmacy
from .serializers import  ProfileSerializer,PharmacySerializer
from rest_framework  import  viewsets
from Chem import serializers
# Create your views here.


class ProfileList(viewsets.ModelViewSet):
               queryset=Profile.objects.all()
               serializer_class=ProfileSerializer

class PharmacyList(viewsets.ModelViewSet):
               queryset=Pharmacy.objects.all()
               serializer_class=PharmacySerializer             

