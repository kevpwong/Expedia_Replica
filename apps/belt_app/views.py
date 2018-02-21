from django.shortcuts import render, HttpResponse, redirect
from models import *
from django.contrib import messages
from sets import Set
import bcrypt

def index(request):
    return render(request, 'belt_app/index.html')

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else: 
        User.objects.create(name=request.POST['name'], username=request.POST['username'], password= bcrypt.hashpw(request.POST['pass'].encode(), bcrypt.gensalt()))
        id = User.objects.get(username=request.POST['username']).id
        request.session['id'] = id
        request.session['username'] = User.objects.get(id=id).name 
    return redirect('/travels')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else: 
        id = User.objects.get(username=request.POST['logname']).id
        request.session['id'] = id
        request.session['username'] = User.objects.get(id=id).username
    return redirect('/travels')

def travels(request):
    all_trips = Place.objects.all()
    user_trips_set = Set([])
    all_trips_set = Set([])
    other_trips = Set([])
    user_trips = []
    other_trips = []

    for trip in all_trips:
        all_trips_set.add(trip.id)     
        for user in trip.users.all(): 
            if str(user.id) == str(request.session['id']):
                user_trips_set.add(trip.id)   

    other_trips_set = all_trips_set.difference(user_trips_set)

    for id in user_trips_set: 
        print id
        trip = Place.objects.filter(id=id)[0]
        addtrip = {
        'id' : trip.id,
        'planner' : trip.planner.name,
        'place' : trip.place, 
        'start' : trip.start,
        'end' : trip.end,
        'description' : trip.description,
        }
        user_trips.append(addtrip)

    for id in other_trips_set: 
        print id
        trip = Place.objects.filter(id=id)[0]
        addtrip = {
        'id' : trip.id,
        'planner' : trip.planner.name,
        'place' : trip.place, 
        'start' : trip.start,
        'end' : trip.end,
        'description' : trip.description,
        }
        other_trips.append(addtrip)

    trips = {
        'user_trips': user_trips,
        'other_trips': other_trips
    }
    return render(request, 'belt_app/travels.html', trips)

def add(request):
    return render(request, 'belt_app/add.html')

def addtrip(request):
    errors = User.objects.add_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/travels/add')
    else: 
        new = Place.objects.create(place=request.POST['place'], description=request.POST['description'], start=request.POST['start'], end=request.POST['end'], planner= User.objects.get(id=request.POST['id']))
        new.users.add(User.objects.get(id=request.POST['id']))
    return redirect('/travels')

def jointrip(request, trip_id):
    trip = Place.objects.filter(id = trip_id)[0]
    trip.users.add(User.objects.get(id=request.session['id']))
    place = Place.objects.filter(id=trip_id)[0]
    others = []
    destination = {
        'place' : place,
        'others' : others
    }
    return redirect('/travels')

def destination(request, id):
    place = Place.objects.filter(id=id)[0]
    others = []
    for user in place.users.all(): 
        if not user.name == place.planner.name:
            others.append(user.name) 
    destination = {
        'place' : place,
        'others' : others
    }
    return render(request, 'belt_app/destination.html', destination)
 
def logout(request):
    request.session.clear()
    return redirect('/')
