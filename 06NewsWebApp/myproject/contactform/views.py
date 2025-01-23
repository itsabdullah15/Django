from django.shortcuts import render, get_object_or_404, redirect
from .models import ContactForm
from news.models import News
from cat.models import Cat
from subcat.models import SubCat
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
import datetime

def contact_add(request):
    #login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    #login check end
    
    current_time = datetime.datetime.now()
    today_date = f"{current_time.year}-{current_time.month:02}-{current_time.day:02}"  # Format: YYYY-MM-DD
    current_time_formatted = f"{current_time.hour}:{current_time.minute}"

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        txt = request.POST.get('msg')
        
        if name == "" or email == "" or txt == "":
            msg = "All Fields are required!"
            return render(request, 'front/msgbox.html', {'msg': msg})
        
        b = ContactForm(name=name, email=email, txt=txt, date=today_date, time=current_time_formatted)
        b.save()
        msg = "Your Message Recieved"
        return render(request, 'front/msgbox.html', {'msg':msg})
    
    return render(request, 'front/msgbox.html')


def contact_show(request):
    #login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    #login check end
    msg = ContactForm.objects.all()
    
    return render(request, 'back/contact_form.html', {'msg':msg})

def contact_del(request, pk):
    #login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    #login check end
    
    b=ContactForm.objects.filter(pk=pk)
    b.delete()
    return redirect('contact_show')
    