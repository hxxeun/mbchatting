from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Room


# def room(request):
#     room_name = Room.objects.all()
#     return render(request, "chat/room.html", {"room_name": room_name})

@login_required
def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})