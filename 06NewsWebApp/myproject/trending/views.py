from django.shortcuts import render, get_object_or_404, redirect
from .models import Trending
from news.models import News
from cat.models import Cat
from subcat.models import SubCat
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage


def trending_add(request):
    #login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    #login check end
    
    if request.method == 'POST':
        txt = request.POST.get('txt')
        if txt == "":
            error = "All Fields Required!"
            return render(request, 'back/error.html', 
                          {'error': error})
        
        b = Trending(txt=txt)
        b.save()
    
    trendinglist = Trending.objects.all()[:5]
    
    return render(request, 'back/trending.html', {'trendinglist': trendinglist})



def trending_del(request, pk):
    b = Trending.objects.filter(pk=pk)
    b.delete()
    
    return redirect('trending_add')




def trending_edit(request, pk):
    trending = get_object_or_404(Trending, pk=pk)

    if request.method == 'POST':
        txt = request.POST.get('txt')
        
        if not txt:
            error = "All Fields Required"
            return render(request, 'back/error.html', {'error': error})
        
        trending.txt = txt
        trending.save()
        return redirect('trending_add')  # Redirect to the list page or another page

    return render(request, 'back/trending_edit.html', {'mytxt': trending.txt, 'pk': pk})
