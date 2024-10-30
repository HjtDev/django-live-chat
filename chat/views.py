import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from account.models import User
from .models import Room
from account.forms import AddUserForm


@require_POST
def create_room(request, uuid):
    name = request.POST.get('name', '')
    url = request.POST.get('url', '')
    Room.objects.create(uuid=uuid, client=name, url=url)

    return JsonResponse({'message': 'Room created'})


@login_required
def delete_room(request, uuid):
    try:
        room = Room.objects.get(uuid=uuid)
        room.messages.all().delete()
        room.delete()
    except Room.DoesNotExist:
        pass
    return redirect('chat:admin_room')


@login_required
def admin_room(request):
    rooms = Room.objects.all()
    users = User.objects.filter(is_staff=True)
    return render(request, 'chat/admin.html', {'rooms': rooms, 'users': users})


@login_required
def room_view(request, uuid):
    room = Room.objects.get(uuid=uuid)
    if room.status == Room.Status.WAITING:
        room.status = Room.Status.ACTIVE
        room.agent = request.user
        room.save()
    return render(request, 'chat/room.html', {"room": room})


@login_required
def add_user(request):
    form = AddUserForm()
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_staff = True
            user.save()
            return redirect('chat:admin_room')
    return render(request, 'chat/add_user.html', {'form': form})


@login_required
def user_view(request, uuid):
    user = User.objects.get(id=uuid)
    rooms = user.rooms.all()
    return render(request, 'chat/user.html', {"user": user, 'rooms': rooms})

