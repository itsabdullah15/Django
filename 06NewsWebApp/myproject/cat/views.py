from django.shortcuts import render, redirect
from .models import Cat
# Create your views here.
def cat_list(request):
    
    #login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    #login check end
    
    cat  = Cat.objects.all()
    return render(request, 'back/cat_list.html', {'cat':cat}) 


def cat_add(request):
    
    #login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    #login check end
    
    if request.method == 'POST':
        # Retrieve the category name from the form
        name = request.POST.get('name')

        # Check if the name field is empty
        if not name:
            error = "Category Filed is required to be filled!"
            return render(request, 'back/error.html', {'error': error})

        # Check if a category with the same title already exists
        if Cat.objects.filter(name=name).exists():
            error = "This title has already been used!"
            return render(request, 'back/error.html', {'error': error})

        # Save the new category to the database
        new_category = Cat(name=name)
        new_category.save()
        return redirect('cat_list')

    # Render the category addition form
    return render(request, 'back/cat_add.html')

