from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
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
    path('MembershipStaff/', views.MembershipStaff,name='MembershipStaff'),
    path('media/pdfs/some_file.pdf/',views.pdf_view, name='pdfs')
 ]
 #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# path('pdf_view/', views.pdf_view,name='pdf_view')
    # PATH('show_pdf/', views.show_pdf, name='show_pdf')