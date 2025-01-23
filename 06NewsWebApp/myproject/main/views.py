from django.shortcuts import render, get_object_or_404, redirect
from .models import Main
from news.models import News
from cat.models import Cat
from subcat.models import SubCat
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.utils.html import strip_tags
from trending.models import Trending
import random
from random import randint
from django.contrib.auth.models import User
from manager.models import Manager
from django.contrib.auth.decorators import login_required



def home(request):
    sitename = Main.objects.get(pk=1)
    news = News.objects.filter(act=1).order_by('-pk')
    cat =  Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.filter(act=1).order_by('-pk')[:3]
    popnews = News.objects.filter(act=1).order_by('-show')
    popnews2 = News.objects.filter(act=1).order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]
    lastnews2 = News.objects.filter(act=1).order_by('-pk')[:4]
    
    
    random_object = Trending.objects.all()[randint(0, len(trending) - 1)]
    
    return render(
        request, 'front/home.html', 
        {
            'sitename': sitename, 
            'news': news, 
            'cat':cat, 
            'subcat':subcat,
            'lastnews': lastnews,
            'popnews': popnews,
            'popnews2': popnews2,
            'trending': trending,
            'lastnews2':lastnews2
        }
    )

def about(request):
    sitename = Main.objects.get(pk=1)
    news = News.objects.all().order_by('-pk')
    cat =  Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.all().order_by('-pk')[:3]
    # popnews = News.objects.all().order_by('-show')
    popnews2 = News.objects.all().order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')
    
    
    return render(
        request, 'front/about.html', 
        {
            'sitename': sitename,
            'news': news, 
            'cat':cat, 
            'subcat':subcat,
            'lastnews': lastnews,
            'popnews2': popnews2,
            'trending': trending
        })

@login_required
def panel(request):
    rand = random.randint(0, 100000)    
    
    return render(request, 'back/home.html')


def mylogin(request):
    if request.method == 'POST':
        utxt = request.POST.get('username')
        ptxt = request.POST.get('password')
        
        if utxt != "" and ptxt != "":
            user = authenticate(username=utxt, password=ptxt)
            
            if user != None:
                login(request, user)
                return redirect('panel')
    return render(request, 'front/login.html')


def myregister(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if name == "" :
            msg = "Input Your Name"
            return render(request, 'front/msgbox.html', {'msg':msg})
        
        if password1 != password2:
            msg = "Your Pass Didn't Match"
            return render(request, 'front/msgbox.html', {'msg': msg})

        error = validate_password(password1)
        if error:
            return render(request, 'back/error.html', {'error': error})

         # Check if the username or email already exists
        if User.objects.filter(username=uname).exists():
            msg = "Username is already taken!"
            return render(request, 'front/msgbox.html', {'msg': msg})

        if User.objects.filter(email=email).exists():
            msg = "Email is already registered!"
            return render(request, 'front/msgbox.html', {'msg': msg})
        
        user = User.objects.create_user(username=uname, email=email, password=password1 )
        b = Manager(name=name,utxt=uname,email=email)
        b.save()
            
    
    return render(request, 'front/login.html')



def mylogout(request):
    logout(request)
    return redirect('mylogin')



def site_setting(request):
    # Check if the user is logged in
    if not request.user.is_authenticated:
        return redirect('my_login')

    site = get_object_or_404(Main, pk=1)

    if request.method == 'POST':
        # Retrieve and validate form data
        name = request.POST.get('name')
        tell = request.POST.get('tell')
        fb = request.POST.get('fb', "#")
        tw = request.POST.get('tw', "#")
        yt = request.POST.get('yt', "#")
        link = request.POST.get('link', "#")
        txt = strip_tags(request.POST.get('txt', ""))

        if not name or not tell or not txt:
            error = "All Fields Required"
            return render(request, 'back/error.html', {'error': error})

        # Helper function for file upload
        def handle_file_upload(file):
            if file:
                file_storage = FileSystemStorage()
                filename = file_storage.save(file.name, file)
                return file_storage.url(filename), filename
            return "-", "-"

        # Handle file uploads
        picurl, picname = handle_file_upload(request.FILES.get('myfile'))
        picurl2, picname2 = handle_file_upload(request.FILES.get('myfile2'))

        # Update site settings
        site.name = name
        site.tell = tell
        site.facebook = fb
        site.twitter = tw
        site.youtube = yt
        site.link = link
        site.about = txt

        if picurl != "-": site.picurl = picurl
        if picname != "-": site.picname = picname
        if picurl2 != "-": site.picurl2 = picurl2
        if picname2 != "-": site.picname2 = picname2

        site.save()

    return render(request, 'back/setting.html', {'site': site})


def about_setting(request):
    # Check if the user is logged in
    if not request.user.is_authenticated:
        return redirect('my_login')
    
    if request.method == 'POST':
        text = request.POST.get('txt')
        if text == "":
            error = "About text field is required!"
            return render(request, 'back/error.html', {'error': error})
        b = Main.objects.get(pk=1)
        b.about_text = text
        b.save()
    
    about = Main.objects.get(pk=1).about_text
    
    return render(request,'back/about_setting.html', 
        {
            'about': about
        })
    
def contact(request):
    sitename = Main.objects.get(pk=1)
    news = News.objects.all().order_by('-pk')
    cat =  Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.all().order_by('-pk')[:3]
    # popnews = News.objects.all().order_by('-show')
    popnews2 = News.objects.all().order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')
    
    
    return render(request, 'front/contact.html', {
        'sitename': sitename,
        'news': news, 
        'cat':cat, 
        'subcat':subcat,
        'lastnews': lastnews,
        'popnews2': popnews2,
        'trending': trending
    })
    
    
    
def change_pass(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect('mylogin')

    if request.method == 'POST':
        old_pass = request.POST.get('oldpass', '').strip()
        new_pass = request.POST.get('newpass', '').strip()

        # Validate input fields
        if not old_pass or not new_pass:
            return render(request, 'back/error.html', {'error': "All fields are required"})

        user = authenticate(username=request.user.username, password=old_pass)

        if user is None:
            return render(request, 'back/error.html', {'error': "Your current password is incorrect"})

        # Validate new password
        error = validate_password(new_pass)
        if error:
            return render(request, 'back/error.html', {'error': error})

        # Change the password
        user = User.objects.get(username=request.user.username)
        user.set_password(new_pass)
        user.save()

        return redirect('mylogout')

    return render(request, 'back/changepass.html')

def validate_password(password):
    if len(password) < 8:
        return "Your password must be at least 8 characters long"

    if not any(char.isdigit() for char in password):
        return "Your password must include at least one number"

    if not any(char.isupper() for char in password):
        return "Your password must include at least one uppercase letter"

    if not any(char.islower() for char in password):
        return "Your password must include at least one lowercase letter"

    if not any(char in "!@#$%^&*()-_=+[]{}|;:',.<>?/~`" for char in password):
        return "Your password must include at least one special character"

    return None

