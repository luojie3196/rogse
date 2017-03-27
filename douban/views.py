from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
import datetime
from douban.models import Douban
from douban.forms import DoubanForm

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
