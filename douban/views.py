from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
import datetime
from douban.models import Douban
from douban.forms import DoubanForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


def home(request):
    now = datetime.datetime.now()
    # html = "<html><body>It is now %s.</body></html>" % now
    # return HttpResponse(html)
    try:
        p = Douban.objects.all()
    except Douban.DoesNotExist:
        raise Http404("Douban does not exist")
    return render(request, 'home.html', {'now': now, 'detail_list': p})


def detail(request, page):
    p_start = int(page) - 20
    p_end = int(page)
    try:
        p = Douban.objects.all()
    except Douban.DoesNotExist:
        raise Http404("Douban does not exist")
    return render(request, 'detail.html', {'detail': p, 'p_start': p_start, 'p_end': p_end})


def next_detail(request):
    print(request.POST)
    p_start = 0
    p_end = 20
    if request.method == 'POST':
        page = int(request.POST['page'])
        if request.POST['action'] == 'next':
            p_start = page
            p_end = page + 20
        if request.POST['action'] == 'previous':
            p_start = page - 20
            p_end = page
    try:
        p = Douban.objects.all()
    except Douban.DoesNotExist:
        raise Http404("Douban does not exist")
    return render(request, 'detail.html', {'detail': p, 'p_start': p_start, 'p_end': p_end})


def movie_form(request):
    form = DoubanForm()
    return render(request, 'movie_form.html', {'movie_form': form})


def listing(request):
    movie_list = Douban.objects.all()
    paginator = Paginator(movie_list, 25)  # Show 25 movies per page

    page = request.GET.get('page')
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        movies = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        movies = paginator.page(paginator.num_pages)

    return render(request, 'list.html', {'movies': movies})
