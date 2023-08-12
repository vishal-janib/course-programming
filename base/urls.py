from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('home/',views.home, name="home"),
    path('room/<str:pk>/',views.room, name="room"),

    path('create-room/',views.createRoom, name="create-room"),
    path('update-room/<str:pk>/',views.updateRoom, name="update-room"),
    path('home/deleteRoom/<str:pk>/',views.deleteRoom),
    #path('register/',views.register, name='register'),
    path('otp/<str:pk>/',views.otp, name='otp'),
    path('otpStaff/<str:pk>/',views.otpStaff, name='otpStaff'),
    path('Membership/', views.Membership,name='Membership'),
    path('MembershipStaff/', views.MembershipStaff,name='MembershipStaff')

]