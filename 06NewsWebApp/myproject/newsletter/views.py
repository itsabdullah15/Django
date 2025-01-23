from django.shortcuts import render, get_object_or_404, redirect
from .models import Newsletter
from news.models import News
from cat.models import Cat
from subcat.models import SubCat
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from trending.models import Trending
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required

# Create your views here.
def news_letter(request):
    
    if request.method == 'POST':
        txt = request.POST.get('txt')
        res = txt.find('@')
        if int(res) != -1 :
            b = Newsletter(txt=txt,status=1)
            b.save()
        else:
            try:
                int(txt)
                b = Newsletter(txt=txt,status=2)
                b.save()
            except:
                return redirect('home')
    return redirect('home')


@login_required
def news_email(request):
    emails = Newsletter.objects.filter(status=1)
    return render(request, 'back/emails.html', {'emails':emails})


@login_required
def news_phones(request):
    phone = Newsletter.objects.filter(status=2)
    return render(request, 'back/emails.html', {'phones':phone})
    
    
@login_required
def news_txt_del(request,pk,num) :
    b = Newsletter.objects.get(pk=pk)
    b.delete()

    if int(num) == 2 :
        return redirect('news_phones') 

    return redirect('news_email') 