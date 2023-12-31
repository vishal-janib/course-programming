from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Room, Topic
from django.http import FileResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import RoomForm, MemberForm
from django.core.mail import send_mail
import random
import os
from django.conf import settings

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.shortcuts import get_object_or_404
from django.templatetags.static import static


def Membership(request):
    email = request.POST.get('email')
    if request.method=='POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        email = request.POST.get('email')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Both passwords should match!!')
            return render(request, 'register.html')
        try:
            user = User.objects.get(email=email)
            messages.error(request, 'User does Exist.')
        except:
            user = User.objects.create_user(
                username=username,
                password=password1,
                email=email
            )
            email = request.POST.get('email')
            return redirect('otp',email)
    return render(request,'base/register.html')

def MembershipStaff(request):
    email = request.POST.get('email')
    if request.method=='POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        email = request.POST.get('email')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Both passwords should match!!')
            return render(request, 'register_staff.html')
        try:
            user = User.objects.get(email=email)
            messages.error(request, 'User does Exist.')
        except:
            user = User.objects.create_superuser(
                username=username,
                password=password1,
                email=email
            )
            email = request.POST.get('email')
            return redirect('otpStaff',email)
    return render(request,'base/register_staff.html')

global no
no=0
def otp(request,pk):
    # user=User.objects.get(email=pk)
    global no
    if request.method == 'POST':
        otp = request.POST.get('otp', '')
        if(int(otp)==int(no)):
            return redirect('login')
        else:
            u = User.objects.get(email=pk)
            u.delete()
            return redirect('Membership')
    else:
        no = random.randrange(1000,9999)
        send_mail('Your OTP for verification','Your OTP is {}'.format(no),'vishaljanib@gmail.com',[pk],fail_silently=False)
        return render(request, 'base/otp.html', {})

no=0
def otpStaff(request,pk):
    # user=User.objects.get(email=pk)
    global no
    if request.method == 'POST':
        otp = request.POST.get('otpStaff', '')
        if(int(otp)==int(no)):
            return redirect('login')
        else:
            u = User.objects.get(email=pk)
            u.delete()
            return redirect('MembershipStaff')
    else:
        no = random.randrange(1000,9999)
        send_mail('Your OTP for verification','Your OTP is {}'.format(no),'vishaljanib@gmail.com',[pk],fail_silently=False)
        return render(request, 'base/otp_staff.html', {})


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not Exist.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'Username or password does not exist')
    context={}
    return render(request, 'base/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    topics = Topic.objects.all()
    context = {'rooms':rooms, 'topics':topics}
    return render(request, 'base/home.html', context)

def room(request,pk):
    room=Room.objects.get(id=pk)
    context={'room':room}
    return render(request, 'base/room.html',context)

@login_required
def createRoom(request):
    form = RoomForm()
    if request.user.is_superuser:
        if request.method=='POST':
            form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        return redirect('home')
    context={'form':form}
    return render(request, 'base/room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render (request, 'base/room_form.html', context)

def pdf_view(request):
    name=request.FILES('name', "")
    filename = "pacewisdom/media/pdfs/"+name+".pdf"
    with open(filename, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type ='application/pdf')
        response['Content-Disposition'] = 'inline;filename=some_file.pdf'
        return response
    pdf.closed

    
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse('You cannot delete!!')

    room.delete()
    return redirect('home')
    
       