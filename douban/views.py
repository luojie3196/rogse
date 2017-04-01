#!/usr/bin/python
# encoding:utf-8

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
import datetime
from douban.models import Douban
from douban.forms import DoubanForm, UserProfileCreationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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


@login_required
def dashboard(request):
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

    return render(request, 'dashboard.html', {'movies': movies})


@login_required
def search(request):
    keywords = request.GET.get('keywords')
    movie_list = Douban.objects.filter(Q(title__icontains=keywords) | Q(director__icontains=keywords) |
                                       Q(region__icontains=keywords) | Q(language__icontains=keywords) |
                                       Q(release_time__icontains=keywords))
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

    return render(request, 'search.html', {'movies': movies, 'keywords': keywords, 'total': len(movie_list)})


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/douban/')
        else:
            return render(request, 'login.html', {'status': '1'})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('/douban/login/')


def register(request):
    form = UserProfileCreationForm()
    if 'status' in request.GET:
        status = request.GET['status']
        return render(request, 'register.html', {'forms': form, 'status': status})
    if request.method == "POST":
        form = UserProfileCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/douban/register/?status=0')
    return render(request, 'register.html', {'forms': form})


@login_required
def reports_page(request):
    return render(request, 'reports.html')


@login_required
def analytics_page(request):
    return render(request, 'analytics.html')


@login_required
def export_page(request):
    return render(request, 'export.html')


@login_required
def settings_page(request):
    return render(request, 'settings.html')


@login_required
def views_page(request):
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

    return render(request, 'views_page.html', {'movies': movies})
