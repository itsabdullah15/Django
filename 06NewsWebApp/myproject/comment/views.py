from django.shortcuts import render, redirect
from .models import Comment
from news.models import News
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group, Permission
from manager.models import Manager

import datetime
from django.contrib.auth.decorators import login_required


# Create your views here.

def news_cm_add(request,pk) :


    if request.method == 'POST':

        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day
        
        if len(str(day)) == 1 :
            day = "0" + str(day)
        if len(str(month)) == 1 :
            month = "0" + str(month)

    
        today = str(year) + "/" + str(month) + "/" + str(day)
        time = str(now.hour) + ":" + str(now.minute)

        cm = request.POST.get('msg')

        if request.user.is_authenticated :
            manager = Manager.objects.get()

            b = Comment(name=manager.name,email=manager.email,cm=cm,news_id=pk,date=today,time=time)
            b.save()

        else:

            name = request.POST.get('name')
            email = request.POST.get('email')

            b = Comment(name=name,email=email,cm=cm,news_id=pk,date=today,time=time)
            b.save()
            

    newsname = News.objects.get(pk=pk).slug

    return redirect('news_detail' , slug=newsname)


@login_required
def comments_list(request, pk=None):
    # Check if the user has permission
    has_permission = any(group.name == "masteruser" for group in request.user.groups.all())

    if not has_permission:
        # Get the author of the specific news item
        news_author = News.objects.get(pk=pk).author
        if str(news_author) != str(request.user):
            error_message = "Access Denied"
            return render(request, 'back/error.html', {'error': error_message})

    # Fetch all comments
    comments = Comment.objects.all()

    return render(request, 'back/comments_list.html', {'comment': comments})




@login_required
def comments_del(request,pk):
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0 :
        a = News.objects.get(pk=pk).author
        if str(a) != str(request.user) :
            error = "Access Denied"
            return render(request, 'back/error.html' , {'error':error})
    

    comment = Comment.objects.filter(pk=pk)
    comment.delete()

    return redirect('comments_list')


@login_required
def comments_confirmed(request,pk):

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0 :
        a = News.objects.get(pk=pk).author
        if str(a) != str(request.user) :
            error = "Access Denied"
            return render(request, 'back/error.html' , {'error':error})
    

    comment = Comment.objects.get(pk=pk)
    comment.status = 1
    comment.save()

    return redirect('comments_list')