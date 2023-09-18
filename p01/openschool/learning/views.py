from django.shortcuts import render, redirect
from . models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from datetime import date

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
#import openai

from .models import DownloadableItem
from .forms import DownloadableItemForm
# Create your views here.


def index(request):
    return render(request, "index.html")

def user_login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                user1 = Student.objects.get(user=user)
                if user1.type == "applicant":
                    login(request, user)
                    return redirect("/user_homepage")
            else:
                thank = True
                return render(request, "user_login.html", {"thank":thank})
    return render(request, "user_login.html")


def user_homepage(request):
    if not request.user.is_authenticated:
        return redirect('/user_login/')
    student = Student.objects.get(user=request.user)
    if request.method=="POST":   
        email = request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        phone = request.POST['phone']
        gender = request.POST['gender']

        student.user.email = email
        student.user.first_name = first_name
        student.user.last_name = last_name
        student.phone = phone
        student.gender = gender
        student.save()
        student.user.save()

        try:
            image = request.FILES['image']
            student.image = image
            student.save()
        except:
            pass
        alert = True
        return render(request, "user_homepage.html", {'alert':alert})
    return render(request, "user_homepage.html", {'student':student})


def signup(request):
    if request.method=="POST":   
        username = request.POST['email']
        email= request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone = request.POST['phone']
        gender = request.POST['gender']
        image = request.FILES['image']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('/signup')
        
        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, password=password1)
        applicants = Student.objects.create(user=user, phone=phone, gender=gender, image=image, type="Student")
        user.save()
        applicants.save()
        return render(request, "user_login.html")
    return render(request, "signup.html")

def Teacher_signup(request):
    if request.method=="POST":   
        username = request.POST['username']
        email = request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone = request.POST['phone']
        gender = request.POST['gender']
        image = request.FILES['image']
        company_name = request.POST['company_name']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('/signup')
        
        user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password1)
        company =Teacher.objects.create(user=user, phone=phone, gender=gender, image=image, company_name=company_name, type="company", status="pending")
        user.save()
        company.save()
        return render(request, "Teacher_login.html")
    return render(request, "Teacher_signup.html")


def Teacher_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            user1 = Teacher.objects.get(user=user)
            if user1.type == "teacher" and user1.status != "pending":
                login(request, user)
                return redirect("/Teacher_homepage")
        else:
            alert = True
            return render(request, "Teacher_login.html", {"alert":alert})
    return render(request, "Teacher_login.html")

def Teacher_homepage(request):
    if not request.user.is_authenticated:
        return redirect("/Teacher_login")
    teacher = Teacher.objects.get(user=request.user)
    if request.method=="POST":   
        email = request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        phone = request.POST['phone']
        gender = request.POST['gender']

        teacher.user.email = email
        teacher.user.first_name = first_name
        teacher.user.last_name = last_name
        teacher.phone = phone
        teacher.gender = gender
        teacher.save()
        teacher.user.save()

        try:
            image = request.FILES['image']
            teacher.image = image
            teacher.save()
        except:
            pass
        alert = True
        return render(request, "Teacher_homepage.html", {'alert':alert})
    return render(request, "Teacher_homepage.html", {'teacher':teacher})



def Logout(request):
    logout(request)
    return redirect('/')




def chat(request):
    chats=Chat.objects.all()
    return render(request,'chat.html',{'chats':chats,
                                       })

@csrf_exempt
def Ajax(request):
    if request.headers.get ('X-Requested-With') =='XMLHttpRequest':

        text = request.POST.get('text')
        print(text)

        openai.api_key="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"    #api key has to be change
        
        res=openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user","content":f"{text}"}
        ]
        )

        response =res.choices[0].message["content"]
        print(response)

        chat = Chat.objects.create(
            text=text,
            gpt=response

        )

        return JsonResponse({'data':response})
    return JsonResponse({})




def upload_downloadable_item(request):
    if request.method == 'POST':
        form = DownloadableItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_downloadable_items')
    else:
        form = DownloadableItemForm()
    return render(request, 'downloads/upload.html', {'form': form})

def list_downloadable_items(request):
    downloadable_items = DownloadableItem.objects.all()
    return render(request, 'downloads/list.html', {'downloadable_items': downloadable_items})

#for post

from .models import Post

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'post_detial.html', {'post': post})