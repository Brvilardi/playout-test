from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User


# Create your views here.

def index(request):
    #Checks if user is not authenticated
    if not request.user.is_authenticated:
        return render(request, "webapp/login.html")

    return render(request, "webapp/index.html", {"user": request.user.username})

def login(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == "GET":
        return render(request, "webapp/login.html")
    user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
    print("User: ", user)
    if user is not None:
        auth_login(request, user)
        return redirect('index')
    return render(request, "webapp/login.html", {"issue": "wrg cred"}) #render login, saying it has wrong credentials

    

def logout(request):
    if request.user.is_authenticated:
        django_logout(request)
    return HttpResponse("user logged out")


def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'GET':
        return render(request, "webapp/registration.html")
    
    #Checks what kind o POST the request is about
    form = request.POST 
    print("form: ", form)
    
    #Checks if the registration request is supposed for only render the html
    if "status" in form.keys():
        if form["status"] == "render_html":
            return render(request, "webapp/registration.html")
        else:
            return HttpResponseNotFound('<h1>Registration request error</h1>')

    #Checks if the registration form had username or email already used
    if User.objects.filter(username=form['username']).exists():
        print("username already exists")
        return render(request, "webapp/registration.html", {"issue": "username"})
    if User.objects.filter(email=form['email']).exists():
        print("email already exists")
        return render(request, "webapp/registration.html", {"issue": "email"})  

    #All info is ok, so the user can be created
    user = User.objects.create_user(username=form["username"], password=form["password"],
                                    email=form["email"], first_name=form["f_name"], last_name=form["l_name"])       
    return HttpResponse("success - user created")




    

    