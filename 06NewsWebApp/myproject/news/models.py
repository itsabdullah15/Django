from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class News(models.Model):
    title = models.CharField(max_length=250, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)  # You can keep unique=True, but it's fine to remove for debugging
    summary = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    publication_date = models.DateField()  
    publication_time = models.CharField(max_length=12, default="00:00")
    imagename = models.ImageField(upload_to='news_images/', null=True, blank=True)  # Image field
    imageurl = models.TextField(default="-")  
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    catname = models.CharField(max_length=50, default='-')
    catid = models.IntegerField(default=0)
    ocatid = models.IntegerField(default=0)
    show = models.IntegerField(default=0)
    tag = models.TextField(default="")
    act = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-publication_date', '-id']
    
    def save(self, *args, **kwargs):
        # Ensure the title is not empty before generating slug
        if not self.title:
            raise ValueError("Title cannot be empty")
        
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            # Check if the slug already exists and generate a unique slug
            while News.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        
        super().save(*args, **kwargs)
    
    @property
    def formatted_date(self):
        return self.publication_date.strftime('%d/%m/%Y')
    
    def __str__(self):
        return self.title
