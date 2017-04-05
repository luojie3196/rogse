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
from douban.commons import M_TYPES, REGIONS, generate_xls, file_download, merge_to_list, \
    generate_map_data, generate_type_data, export_xls

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
    search_mode = True
    try:
        keywords = request.GET['keywords']
    except KeyError:
        movie_list = Douban.objects.all()
        search_mode = False
    else:
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
    if search_mode:
        return render(request, 'search.html', {'movies': movies, 'keywords': request.GET['keywords'],
                                               'total': len(movie_list)})
    else:
        return render(request, 'dashboard.html', {'movies': movies})


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
    # movie_data = Douban.objects.all()
    # map_data = generate_map_data(movie_data)
    # type_dict = generate_type_data(movie_data)
    # regions = merge_to_list(p.region for p in movie_data)
    # return render(request, 'analytics.html', {'map_data': map_data})
    return render(request, 'analytics.html')


@login_required
def export_page(request):
    filter_mode = True
    rows_num_list = ['25', '50', '100', '250', '500', '1000', '5000']
    movie_list = Douban.objects.all()
    # Export file code
    try:
        start_index = request.GET['start_index']
        end_index = request.GET['end_index']
    except KeyError:
        pass
    else:
        if end_index not in rows_num_list or start_index > end_index:
            return HttpResponseRedirect('/douban/export/')
        # generate excel first and then download it
        # file_name_path = generate_xls(movie_list, start_index, end_index)
        # return file_download(file_name_path)

        # export excel file directly by BytesIO stream
        return export_xls(movie_list, start_index, end_index)

        # the second way download file
        # from django.views.static import serve
        # import os
        # return serve(request, os.path.basename(file_name_path), os.path.dirname(file_name_path))
    try:
        rows_num = request.GET['rows_num']
    except KeyError:
        paginator = Paginator(movie_list, 25)  # Default show 25 movies per page
        filter_mode = False
    else:
        try:
            rows_num_list.remove(rows_num)
        except ValueError:
            return HttpResponseRedirect('/douban/export/')
        paginator = Paginator(movie_list, rows_num)

    page = request.GET.get('page')
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        movies = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        movies = paginator.page(paginator.num_pages)
    if filter_mode:
        return render(request, 'export.html', {'movies': movies, 'total': len(movie_list),
                                               'rows_num': request.GET['rows_num'], 'rows_num_list': rows_num_list})
    return render(request, 'export.html', {'movies': movies, 'total': len(movie_list), 'rows_num_list': rows_num_list})


@login_required
def settings_page(request):
    return render(request, 'settings.html')


@login_required
def views_page(request):
    search_mode = True
    try:
        m_type = request.GET['m_type']
        keywords = request.GET['keywords']
        region = request.GET['region']
    except KeyError:
        movie_list = Douban.objects.all()
        search_mode = False
    else:
        movie_list = Douban.objects.filter((Q(title__icontains=keywords) | Q(director__icontains=keywords) |
                                            Q(scriptwriter__icontains=keywords) | Q(protagonist__icontains=keywords)) &
                                           Q(m_type__icontains=m_type) & Q(region__icontains=region))
    # get m_type and region from douban objects
    '''
    m_types = merge_to_list(p.m_type for p in movie_list)
    regions = merge_to_list(p.region for p in movie_list)
    define m_type and regon by code in commons.py
    '''
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
    if search_mode:
        return render(request, 'views_search_page.html',
                      {'movies': movies, 'm_types': M_TYPES, 'regions': REGIONS,
                       'm_type': request.GET['m_type'], 'region': request.GET['region'],
                       'keywords': request.GET['keywords'], 'total': len(movie_list)})
    else:
        return render(request, 'views_page.html',
                      {'movies': movies, 'm_types': M_TYPES, 'regions': REGIONS})

