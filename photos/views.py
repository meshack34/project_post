
from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404
import datetime as dt
from .models import Article
from .models import photos

# Create views
from django.http import HttpResponse, Http404,HttpResponseRedirect
def news_today(request):
    date = dt.date.today()
    news = Article.todays_news()
    return render(request, 'my-photos/daily-photos.html', {"date": date,"news":news})


def index(request):
    # imports photos and save it in database
    photo = photos.objects.all()
    # adding context 
    ctx = {'photo':photo}
    return render(request, 'my-photos/index.html', ctx)



def past_days_news(request,past_date):
    
    try:
        # Converts data from the string Url
        date = dt.datetime.strptime(past_date,'%Y-%m-%d').date()
    except ValueError:
        # Raise 404 error when ValueError is thrown
        raise Http404()
        assert False

    if date == dt.date.today():
        return redirect(news_today)
    
    news = Article.days_news(date)
    return render(request, 'my-photos/my-gallery.html', {"date":date,"news":news})

def search_results(request):

    if 'photo' in request.GET and request.GET["photo"]:
        search_term = request.GET.get("photo")
        searched_photos = photos.search_by_category(search_term)
        message = f"{search_term}"

        return render(request, 'my-photos/search.html',{"message":message,"photos": searched_photos})

    else:
        message = "You haven't searched for any term"
        return render(request, 'my-photos/search.html',{"message":message})

def article(request,article_id):
    try:
        article = Article.objects.get(id = article_id)
    except DoesNotExist:
        raise Http404()
    return render(request,"my-photos/article.html", {"article":article})




