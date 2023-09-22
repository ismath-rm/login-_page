from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.decorators.cache import cache_control



# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
     return render(request,'contact.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def handlelogin(request):
    
    if request.user.is_authenticated:
        return redirect('index')
    if request.method=="POST":
        user_name=request.POST.get("username")
        pass1=request.POST.get("pass1")
        print(user_name,pass1)
        myuser=authenticate(username=user_name,password=pass1)

        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Login Success")
            return redirect('index')
        else:
            messages.error(request,"Invalid Credentails")
            return redirect('/login')

    return render(request,'login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def handlesignup(request):
    
    if request.user.is_authenticated:
        return redirect('index')
    if request.method=="POST":
        user_name=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("pass1")
        confirm_password=request.POST.get("pass2")
        #print(user_name,email,password,confirm_password)
        if password!= confirm_password:
            messages.warning(request,"Password Is Incorrect")
            return redirect('/signup')


        try:
            if User.objects.get(username=user_name):
                messages.info(request,"Username Is Taken")
                return redirect('/signup')

        except:
            pass    

        try:
            if User.objects.get(email=email):
                 messages.info(request,"Email Is Taken")
                 return redirect('/signup')
        except:
            pass    

        myuser=User.objects.create_user(user_name,email,password)
        myuser.save()
        messages.success(request,"Signup Success Please Login")
        return redirect('/login')       

    return render(request,'signup.html')  

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def handlelogout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect('/login')