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
        return HttpResponse("user authenticated")
    
    if request.method == "GET":
        return render(request, "webapp/login.html")
    print("chegou aqui")
    user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
    print("passou pelo user: ", user)
    if user is not None:
        auth_login(request, user)
        return HttpResponse(request.POST["username"] +" have logged succesfuly")
    return HttpResponse("deu ruim no login")

    

def logout(request):
    if request.user.is_authenticated:
        print("antes: ", request.user.is_authenticated)
        django_logout(request)
        print("depois: ", request.user.is_authenticated)
    return HttpResponse("user loged out")


def register(request):
    if request.user.is_authenticated:
        return render(request, "webapp/index.html")

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
    return HttpResponse("success")



#def home(request):
    

    