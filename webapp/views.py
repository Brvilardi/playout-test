from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from .models import Video
from .forms import UploadFileForm


# Create your views here.

def index(request):
    #Checks if user is not authenticated
    if not request.user.is_authenticated:
        return render(request, "webapp/login.html")

    return redirect('home')

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "GET":
        return render(request, "webapp/login.html")
    user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
    print("User: ", user)
    if user is not None:
        auth_login(request, user)
        return render(request, "webapp/success.html", {"message" :"logged in successfully!"})
    return render(request, "webapp/login.html", {"issue": "wrg cred"}) #render login, saying it has wrong credentials

    

def logout(request):
    if request.user.is_authenticated:
        django_logout(request)
    return render(request, "webapp/success.html",{"message": "You've logged out"})


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'GET':
        return render(request, "webapp/registration.html")
    
    #Checks what kind o POST the request is about
    form = request.POST 
    # print("form: ", form)
    
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
    User.objects.create_user(username=form["username"], password=form["password"],
                            email=form["email"], first_name=form["f_name"], last_name=form["l_name"])       
    return render(request, "webapp/success.html", {"message": "You've successfully created an account"})

def home(request):
    #If user is not authenticated, redirects to login page
    if not request.user.is_authenticated:
        return redirect('login')
    

    form = UploadFileForm() #creates empty form

    return render(request, "webapp/home.html", {"form": form})

def video_upload(request):

    if request.method == 'POST':
        print("files: ", request.FILES.keys())
        print("posts: ", request.POST.keys())   
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            video_file = request.FILES['file']
            n_videos = Video.objects.filter(ownear=request.user).count()
            video_file.name = request.user.username + str(n_videos) + ".mp4"
            print("file name: ", video_file.name)
            video = Video(video=video_file, title=request.POST["title"], ownear=request.user)
            video.save()
            return render(request, "webapp/success.html", {"message": "video uploaded"})
        return HttpResponse("something went wrong with your upload =(")


def your_videos(request):
    if not request.user.is_authenticated:
        return redirect('login')   
    videos = Video.objects.filter(ownear__in=User.objects.filter(username=request.user.username))
    print(videos)
    return render(request, "webapp/your_videos.html", {"videos": videos})


def debug(request):
    raise Exception("Entrou em debug")

















    # form = request.POST
    # video = Video(title=form["title"], video=form["video"], ownear=request.user)
    # video.save()
    # return render(request, "webapp/success.html", {"message": "video uploaded"})

    # form = UploadFileForm(request.POST, request.FILES)
    
        # handle_uploaded_file(request.FILES['file'])

    # print("files: ", request.POST["video"])
    # print("posts: ", request.POST.keys())   
    # video = Video(title=request.POST["title"], video=request.POST["video"], ownear=request.user)
    # video.save()

    # with open(f'{request.POST["title"]}.DVR', 'wb+') as destination:
    #     for chunck in request.POST["video"].chuncks():
    #         destination.write(chunk)



    
    return render(request, "webapp/success.html", {"message": "video uploaded"})

    

    