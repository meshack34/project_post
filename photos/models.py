from django.db import models
import datetime as dt

# Create your models here.
class Editor(models.Model):
    first_name = models.CharField(max_length =30 ,null=True)
    last_name = models.CharField(max_length =30 ,null=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length = 10,blank =True)

    def __str__(self):
        return self.first_name
    class meta:
        ordering =['name']
    
    def save_editor(self):
        self.save()


class tags(models.Model):
    name = models.CharField(max_length =30, null=True)

    def __str__(self):
        return self.name

from cloudinary.models import CloudinaryField


class Category(models.Model):
    # title field
    name = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.name
class Location(models.Model):
    # title field
    name = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.name

class photos(models.Model):
    
    title = models.CharField(max_length=100)
    details = models.TextField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    image = CloudinaryField('image',null=True)
    pub_date = models.DateTimeField(auto_now_add=True ,null=True)
    @classmethod
    def search_by_category(cls,search_term):
        news = cls.objects.filter(category__name__icontains=search_term)
        return news


    
class Article(models.Model):
    
    title = models.CharField(max_length =60, null=True)
    post = models.TextField(null=True)
    editor = models.ForeignKey(Editor, on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(tags)
    pub_date = models.DateTimeField(auto_now_add=True, null=True)
    photo_imagen = models.ImageField(upload_to = 'articles/', null=True)

    def __str__(self):
        return self.title
    @classmethod
    def todays_news(cls):
        today = dt.date.today()
        news = cls.objects.filter(pub_date__date = today)
        return news
    
    @classmethod
    def days_news(cls,date):
        news = cls.objects.filter(pub_date__date = date)
        return news
    
    def __str__(self):
        return self.title
   


