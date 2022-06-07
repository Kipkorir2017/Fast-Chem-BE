from django.urls import path, include
from . import views
from rest_framework import routers

from .views import ChangePasswordView
from knox import views as knox_views
from .views import LoginAPI
from django.urls import path

router=routers.DefaultRouter()
router.register('profile',views.ProfileList )
router.register('pharmacy',views.PharmacyList )

urlpatterns=[

    path('api/',include(router.urls)),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('request-reset-email/', views.RequestPasswordResetEmail.as_view(),name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',views.PasswordTokenCheckAPI.as_view(),name = 'password-reset-confirm'),
    path('password-reset-complete', views.SetNewPasswordAPIView.as_view(),name='password-reset-complete')

]