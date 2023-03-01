from django.shortcuts import render, redirect, HttpResponse
from .models import Room, Topic, Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import UserForm

# Create your views here.


def home(request):
    q = request.GET.get("q", "")
    rooms = Room.objects.all()
    topics = Topic.objects.all()
    if q:
        rooms = rooms.filter(
            Q(topic__name__icontains=q)
            | Q(name__icontains=q)
            | Q(description__icontains=q)
        )
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    rooms_count = rooms.count()
    context = {
        "rooms": rooms,
        "topics": topics,
        "rooms_count": rooms_count,
        "room_messages": room_messages,
    }
    return render(request, "core/home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by("-created")
    if request.method == "POST":
        room_messages = Message.objects.create(
            user=request.user, room=room, body=request.POST.get("body")
        )
        room.participants.add(request.user)
        return redirect("core:room", pk=room.id)
    participants = room.participants.all()
    context = {
        "room": room,
        "room_messages": room_messages,
        "participants": participants,
    }
    return render(request, "core/room.html", context)


@login_required(login_url="core:login")
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
            topic=topic,
        )

        return redirect("core:home")

    context = {"form": form, "topics": topics}
    return render(request, "core/room_form.html", context)


@login_required(login_url="core:login")
def edit_room(request, pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("Your are not allowed ")
    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get("name")
        room.topic = topic
        room.description = request.POST.get("description")
        room.save()
        return redirect("core:home")
    context = {"form": form, "topics": topics, "room": room}
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


@login_required(login_url="core:login")
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("Your are not allowed ")
    if request.method == "POST":
        message.delete()
        return redirect("core:home")
    return render(request, "core/delete.html", {"obj": message})


def user_profile(request, pk):
    user = User.objects.get(id=pk)
    topics = Topic.objects.all()
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    context = {
        "user": user,
        "rooms": rooms,
        "room_messages": room_messages,
        "topics": topics,
    }
    return render(request, "core/profile.html", context)


@login_required(login_url="core:login")
def edit_user(request):
    form = UserForm(instance=request.user)
    if request.method == "POST":
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("core:home")
    context = {"form": form}
    return render(request, "core/edit-user.html", context)
