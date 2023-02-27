from django.shortcuts import render, redirect, HttpResponse
from .models import Room, Topic
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

# Create your views here.


def home(request):
    q = request.GET.get("q", 0)
    rooms = Room.objects.all()
    topics = Topic.objects.all()
    if q:
        rooms = rooms.filter(
            Q(topic__name__icontains=q)
            | Q(name__icontains=q)
            | Q(description__icontains=q)
        )
    rooms_count = rooms.count()
    context = {"rooms": rooms, "topics": topics, "rooms_count": rooms_count}
    return render(request, "core/home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {"room": room}
    return render(request, "core/room.html", context)


@login_required(login_url="core:login")
def create_room(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("core:home")

    context = {"form": form}
    return render(request, "core/room_form.html", context)


@login_required(login_url="core:login")
def edit_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("Your are not allowed ")
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("core:home")
    context = {"form": form}
    return render(request, "core/room_form.html", context)


@login_required(login_url="core:login")
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("Your are not allowed ")
    if request.method == "POST":
        room.delete()
        return redirect("core:home")
    return render(request, "core/delete.html", {"obj": room})


def sign_in(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("core:home")
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("core:home")
        else:
            messages.error(request, "Username or Password does not exist")
    context = {"page": page}
    return render(request, "core/login_register.html", context)


def sign_up(request):
    page = "register"
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("core:home")
        else:
            messages.error(request, "An error occured during registration")
    context = {"form": form}
    return render(request, "core/login_register.html", context)


def log_out(request):
    logout(request)
    return redirect("core:home")
