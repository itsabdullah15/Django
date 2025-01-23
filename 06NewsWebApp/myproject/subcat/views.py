from django.shortcuts import render, redirect
from .models import SubCat
from cat.models import Cat

# View for displaying the list of subcategories
def subcat_list(request):
    
    #login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    #login check end
    
    
    subcategories = SubCat.objects.all() # Fetch all subcategories from the database
    return render(request, 'back/subcat_list.html', {'subcat': subcategories})

# View for adding a new subcategory
def subcat_add(request):
    
    #login check start
    if not request.user.is_authenticated:
        return redirect('my_login')
    #login check end
    
    categories = Cat.objects.all() # Fetch all categories to display in the form

    if request.method == 'POST':
        # Retrieve the name and selected category ID from the form
        subcategory_name = request.POST.get('name')
        selected_catid = request.POST.get('cat')

        # Validate that the name field is not empty
        if not subcategory_name:
            error_message = "Category field is required to be filled!"
            return render(request, 'back/error.html', {'error': error_message})

        # Check if a subcategory with the same name already exists
        if SubCat.objects.filter(name=subcategory_name).exists():
            error_message = "This title has already been used!"
            return render(request, 'back/error.html', {'error': error_message})

        # Retrieve the category name based on the selected ID
        category_name = Cat.objects.get(pk=selected_catid).name

        # Create and save the new subcategory
        new_subcategory = SubCat(name=subcategory_name, catname=category_name, catid=selected_catid)
        new_subcategory.save()

        # Redirect to the subcategory list page after successful addition
        return redirect('subcat_list')

    # Render the subcategory addition form with available categories
    return render(request, 'back/subcat_add.html', {'cat': categories})
