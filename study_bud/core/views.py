from django.shortcuts import render

# Create your views here.

rooms = [
    {"id": 1, "name": "Lets Learn python!"},
    {"id": 2, "name": "Design with me"},
    {"id": 3, "name": "Frontend developpers"},
]


def home(request):
    context = {"rooms": rooms}
    return render(request, "core/home.html", context)


def room(request, pk):
    room = None
    for r in rooms:
        if r["id"] == pk:
            room = r
    context = {"room": room}
    return render(request, "core/room.html", context)
