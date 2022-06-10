from django.shortcuts import render
from rest_framework import serializers
from rest_framework .response import Response
from .models import Profile, Pharmacy
from .serializers import  ProfileSerializer,PharmacySerializer,ChangePasswordSerializer,ResetPasswordEmailRequestSerializer,SetNewPasswordSerializer

from rest_framework  import  viewsets
from Chem import serializers
from .utils import Util
from rest_framework.response import Response
from rest_framework  import  viewsets,status,generics,permissions,filters,serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from rest_framework.authtoken.serializers import AuthTokenSerializer

from .views import LoginView as KnoxLoginView
from .models import Profile,Pharmacy
# from mpesa.models import PaymentConfirmation

from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.tokens import PasswordResetTokenGenerator 
from django.utils.encoding import smart_str,force_str,smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse 
# from .utils import Util
from django.shortcuts import redirect
from django.http import HttpResponsePermanentRedirect
# Create your views here.


class ProfileList(viewsets.ModelViewSet):
               queryset=Profile.objects.all()
               serializer_class=ProfileSerializer

class PharmacyList(viewsets.ModelViewSet):
               queryset=Pharmacy.objects.all()
               serializer_class=PharmacySerializer             


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetEmail(generics.GenericAPIView):

    serializer_class = ResetPasswordEmailRequestSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://'+current_site + relativeLink
            email_body = 'CrowdFund \n Hello, \n Use the link below to reset your password and use the given token and uuid \n' + \
                absurl+"?redirect_url="+redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        

class PasswordTokenCheckAPI(generics.GenericAPIView):

    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user,token):
                return Response({'error': 'Token is not valid, please request a new one'},status=status.HTTP_401_UNAUTHORIZED)

            return Response({'success':True, 'message':'Credentials Valid','uidb64':uidb64,'token':token},status=status.HTTP_200_OK)
 
        except DjangoUnicodeDecodeError :
             return Response({'error': 'Token is not valid, please request a new one'},status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


