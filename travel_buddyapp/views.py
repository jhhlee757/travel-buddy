from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from .models import User, Trip, Message, Comment
import bcrypt
from django.db.models import Q
from django.core.files.storage import FileSystemStorage

# Create your views here.
def home(request):
    return redirect('/main')

def main(request):
    return render(request, 'main.html')

def register(request):
    errors = User.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        password = request.POST['password']
        hashpass = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(name = request.POST['name'], username = request.POST['username'],
        password = hashpass)
        request.session['loggedID'] = user.id
        return redirect('/events')

def login(request):
    errors = User.objects.validator2(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        user = User.objects.filter(username = request.POST['username'])
        if len(user) > 0:
            logged_user = user[0]
            request.session['loggedID'] = logged_user.id
    return redirect('/events')

def events(request):
    if 'loggedID' in request.session:
        user = User.objects.get(id = request.session['loggedID'])
        trip = Trip.objects.filter(Q(creator = user) | Q(participants = user))
        othertrips = Trip.objects.exclude(Q(creator = user) | Q(participants = user))
        context = {
            'user' : user,
            'trip': trip,
            'othertrips': othertrips
        }
        return render(request, 'travels.html', context)
    else:
        return redirect('/')

def addpage(request):
    return render(request, 'add.html')

def add(request):
    user = User.objects.get(id = request.session['loggedID'])
    errors = Trip.objects.validator3(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/events/add")
    else:
        trip = Trip.objects.create(destination = request.POST['dest'],
        travel_start_date = request.POST['travel_from'], travel_end_date = request.POST['travel_to'],
        plan = request.POST['desc'], creator = user)
        request.session['loggedID'] = user.id
        context = {
            'trip' : trip
        }

    return redirect('/events', context)

def destination(request, tripid):
    trip = Trip.objects.get(id = tripid)
    user = User.objects.get(id = request.session['loggedID'])
    message = Message.objects.all()
    context = {
        "trip": trip,
        'user': user,
        'message': message
    }
    return render(request, 'tripinfo.html', context)

def join(request, tripid):
    userToAdd = User.objects.get(id = request.session['loggedID'])
    trip = Trip.objects.get(id = tripid)
    trip.participants.add(userToAdd)
    return redirect('/events')

def logout(request):
    request.session.clear()
    return redirect('/')

def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['image']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        url = fs.url(name)

    return redirect('/events/add')

def postmessage(request, tripid):
    user = User.objects.get(id = request.session['loggedID'])
    tripID = Trip.objects.get(id = tripid)
    message = Message.objects.create(user_id = user, trip_id = tripID, messages = request.POST['messagepost'])
    context = {
        'message': message,
        'user': user
    }
    return redirect('/events/destination/' + str(tripid), context)

def postcomment(request, messageid):
    user = User.objects.get(id = request.session['loggedID'])
    message = Message.objects.get(id = messageid)
    comment = Comment.objects.create(message_id = message, user_id = user,
    comments = request.POST['commentpost'])
    return redirect('/events/destination/<tripid>')

def deletemessage(request, userid, tripid):
    message = Message.objects.get(id = userid)
    message.delete()
    return redirect('/events/destination/' + str(tripid))
