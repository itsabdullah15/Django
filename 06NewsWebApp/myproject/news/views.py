from django.shortcuts import render, get_object_or_404, redirect
from .models import News
from main.models import Main
from django.core.files.storage import FileSystemStorage
import datetime
from datetime import datetime
from django.contrib.auth.decorators import login_required
from subcat.models import SubCat
from django.core.exceptions import ValidationError
from cat.models import Cat
from trending.models import Trending
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from comment.models import Comment



def news_details(request, slug):
    site = Main.objects.get(pk=1)
    news = get_object_or_404(News.objects.order_by('-pk'), slug=slug)
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.all().order_by('-pk')[:3]
    popnews = News.objects.all().order_by('-show')
    popnews2 = News.objects.all().order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]
    
    
    tagname = News.objects.get(slug=slug).tag
    tag = tagname.split(',')
    
    
    mynews = News.objects.get(slug=slug)
    mynews.show = mynews.show + 1
    mynews.save()
    
    code = News.objects.get(slug=slug).pk
    comment = Comment.objects.filter(news_id=code, status=1).order_by('-pk')[:3]
    cmcount = len(comment)
    
    # shownews = News.objects.filter(slug=slug)
    
    return render(request, 'front/news_details.html', 
                  {
                      'sitename': site,
                      'news_detail': news, 
                      'cat': cat,
                      'subcat': subcat,
                      'lastnews': lastnews,
                      'popnews': popnews,
                      'popnews2': popnews2,
                      'tag': tag,
                      'trending': trending,
                      'code': code,
                      'comment': comment,
                      'cmcount': cmcount
                      
                    #   'shownews': shownews
                      }
                  )

@login_required
def news_list(request):
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0 :
        news = News.objects.filter(author=request.user)
    elif perm == 1 :
        newss = News.objects.all()
        paginator = Paginator(newss,1)
        page = request.GET.get('page')

        try:
            news = paginator.page(page)

        except EmptyPage :
            news = paginator.page(paginator.num_page)

        except PageNotAnInteger :
            news = paginator.page(1)
    

    return render(request, 'back/news_list.html', {'news':news})



@login_required
def news_add(request):
    categories = SubCat.objects.all()

    # Get the current date and time
    now = datetime.now()
    year, month, day = now.year, f"{now.month:02}", f"{now.day:02}"

    # Format the current date and time
    today_date = f"{year}-{month}-{day}"  # Date in YYYY/MM/DD format
    current_time = f"{now.hour}:{now.minute}"  # Time in HH:MM format

    print("RANDOM")
    # Generate a unique 'rand' value
    date = f"{year}{month}{day}"
    # rand = None  # Initialize the variable
    # while True:
    #     randint = str(random.randint(1000, 9999))
    #     rand = int(date + randint)  # Combine the date and random number
    #     if not News.objects.filter(rand=rand).exists():
    #         break  # Exit loop if 'rand' is unique

    # print("RANDDDDD", rand)
        
        

    if request.method == 'POST':
        # Extract form data
        title = request.POST.get('newstitle')
        category_id = request.POST.get('newscat')
        summary = request.POST.get('newssummary')
        content = request.POST.get('newscontent')
        tag = request.POST.get('tag')

        # Validate mandatory fields
        if not all([title, category_id, summary, content]):
            return render(request, 'back/error.html', {'error': 'Please fill in all required fields.'})

        try:
            # Initialize optional image variables
            image_name = None
            image_url = None

            # Handle file upload if provided
            if 'myfile' in request.FILES:
                uploaded_file = request.FILES['myfile']
                file_storage = FileSystemStorage()
                image_name = file_storage.save(uploaded_file.name, uploaded_file)
                image_url = file_storage.url(image_name)

                # Validate file type
                if not uploaded_file.content_type.startswith("image"):
                    file_storage.delete(image_name)
                    return render(request, 'back/error.html', {'error': 'Only image files are allowed.'})

                # Validate file size
                if uploaded_file.size > 500000:  # 500 KB limit
                    file_storage.delete(image_name)
                    return render(request, 'back/error.html', {'error': 'File size must not exceed 500 KB.'})

            # Retrieve category details
            category = SubCat.objects.get(pk=category_id)
            category_name = category.name
            parent_category_id = category.catid

            # Save the news entry
            news_entry = News(
                title=title,
                summary=summary,
                content=content,
                publication_date=today_date,
                imagename=image_name or '',
                imageurl=image_url or '',
                author=request.user,
                catname=category_name,
                catid=category_id,
                show='0',
                publication_time=current_time,
                ocatid=parent_category_id,
                tag=tag,
            )

            news_entry.save()

            # Update the parent category count
            news_count = News.objects.filter(ocatid=parent_category_id).count()
            parent_category = Cat.objects.get(pk=parent_category_id)
            parent_category.count = news_count
            parent_category.save()

            return redirect('news_list')

        except Exception as error:
            # Clean up uploaded file if an error occurs
            if 'image_name' in locals() and image_name:
                file_storage.delete(image_name)
            return render(request, 'back/error.html', {'error': f'An error occurred: {error}'})

    return render(request, 'back/news_add.html', {'cat': categories})



@login_required
def news_edit(request, pk):
    # Check if the news article exists
    if not News.objects.filter(pk=pk).exists():
        return render(request, 'back/error.html', {'error': "News not found"})

    # Check user permissions
    is_masteruser = request.user.groups.filter(name="masteruser").exists()
    if not is_masteruser:
        article_writer = News.objects.get(pk=pk).author
        if str(article_writer) != str(request.user):
            return render(request, 'back/error.html', {'error': "Access Denied"})

    # Retrieve the news article and categories
    news_article = News.objects.get(pk=pk)
    categories = SubCat.objects.all()

    if request.method == 'POST':
        # Get form data
        title = request.POST.get('newstitle')
        category_id = request.POST.get('newscat')
        summary = request.POST.get('newssummary')
        content = request.POST.get('newscontent')
        tag = request.POST.get('tag')

        # Validate required fields
        if not all([title, category_id, summary, content]):
            return render(request, 'back/error.html', {'error': "All fields are required."})

        try:
            # Handle file upload if provided
            uploaded_file = request.FILES.get('myfile')
            if uploaded_file:
                # Validate file type and size
                if not uploaded_file.content_type.startswith("image"):
                    return render(request, 'back/error.html', {'error': 'Invalid file type. Only images are allowed.'})
                if uploaded_file.size > 500000:
                    return render(request, 'back/error.html', {'error': 'File size must not exceed 500 KB.'})

                # Remove the old image if it exists
                if news_article.imagename:
                    news_article.imagename.delete(save=False)

                # Save the new file
                fs = FileSystemStorage()
                filename = fs.save(uploaded_file.name, uploaded_file)
                image_url = fs.url(filename)

                # Update image fields
                news_article.imagename = filename
                news_article.imageurl = image_url

            # Retrieve category details
            try:
                category = SubCat.objects.get(pk=category_id)
            except SubCat.DoesNotExist:
                return render(request, 'back/error.html', {'error': "Invalid category selected."})

            # Update news article details
            news_article.title = title
            news_article.summary = summary
            news_article.content = content
            news_article.catname = category.name
            news_article.catid = category_id
            news_article.tag = tag
            if not news_article.author:
                news_article.author = request.user
            news_article.act = 0
            news_article.save()

            # Redirect to the news list
            return redirect('news_list')

        except ValidationError as e:
            return render(request, 'back/error.html', {'error': f"Validation error: {e}"})
        except Exception as e:
            return render(request, 'back/error.html', {'error': f"An unexpected error occurred: {e}"})

    # Render the edit form
    return render(request, 'back/news_edit.html', {
        'pk': pk,
        'news': news_article,
        'categories': categories
    })




@login_required
def news_publish(request,pk):
    news = News.objects.get(pk=pk)
    news.act = 1
    news.save()

    return redirect('news_list')







@login_required
def news_delete(request, pk):
    
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0 :
        a = News.objects.get(pk=pk).author
        if str(a) != str(request.user) :
            error = "Access Denied"
            return render(request, 'back/error.html' , {'error':error})
    
    
    news = get_object_or_404(News, id=pk)
    try:
        if news.imagename:
            news.imagename.delete()  # Deletes the file from storage

        # Retrieve the associated category and update the count
        ocatid = news.ocatid
        count = len(News.objects.filter(ocatid=ocatid))
        news_entry = Cat.objects.get(pk=ocatid)
        news_entry.count = count
        news_entry.save()

        # Deleting the news entry
        news.delete()
        return redirect('news_list')
    except Exception as e:
        return render(request, 'back/error.html', {'error': f"An error occurred while deleting the news: {e}"})




def news_all_show(request,slug):

    catid = Cat.objects.get(name=slug).pk
    allnews = News.objects.filter(ocatid=catid)

    site = Main.objects.get(pk=2)
    news = News.objects.filter(act=1).order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.filter(act=1).order_by('-pk')[:3]
    popnews = News.objects.filter(act=1).order_by('-show')
    popnews2 = News.objects.filter(act=1).order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]
    lastnews2 = News.objects.filter(act=1).order_by('-pk')[:4]

    return render(request, 'front/all_news.html', {'site':site, 'news':news, 'cat':cat, 'subcat':subcat, 'lastnews':lastnews, 'popnews':popnews, 'popnews2':popnews2, 'trending':trending, 'lastnews2':lastnews2, 'allnews':allnews})

