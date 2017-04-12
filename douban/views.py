#!/usr/bin/python
# encoding:utf-8

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import datetime
from douban.models import Douban
from douban.forms import DoubanForm, UserProfileCreationForm, UserProfileChangeForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from douban.commons import *
from django.core.mail import send_mail


# Create your views here.


def home(request):
    now = datetime.datetime.now()
    return render(request, 'home.html', {'now': now})


@login_required
def dashboard(request):
    search_mode = True

    sort_by, sort_order = list_sort(request)
    # get keywords, filter query if yes, otherwise skip
    try:
        keywords = request.GET['keywords']
    except KeyError:
        movie_list = Douban.objects.order_by(sort_by)
        search_mode = False
    else:
        movie_list = Douban.objects.filter(Q(title__icontains=keywords) | Q(director__icontains=keywords) |
                                           Q(region__icontains=keywords) | Q(language__icontains=keywords) |
                                           Q(release_time__icontains=keywords)).order_by(sort_by)
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
        total = movie_list.count()
        return render(request, 'search.html', context=locals())
    return render(request, 'dashboard.html', context=locals())


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'status': '1'})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login_page')


def register(request):
    form = UserProfileCreationForm()
    if 'status' in request.GET:
        status = request.GET['status']
        return render(request, 'register.html', locals())
    if request.method == "POST":
        form = UserProfileCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('?status=0')
    return render(request, 'register.html', locals())


@login_required
def reports_page(request):
    form = DoubanForm()
    return render(request, 'reports.html', {'movie_form': form})


@login_required
def analytics_page(request):
    movie_obj = Douban.objects.all()
    map_data = generate_map_data(movie_obj.only('region'))
    type_name, type_num = generate_type_data(movie_obj.only('m_type'))
    # regions = merge_to_list(p.region for p in movie_data)
    year_data, year_name, year_num = generate_years_data(movie_obj.only('release_time'))

    return render(request, 'analytics.html', context=locals())


@login_required
def export_page(request):
    filter_mode = True
    rows_num_list = ['25', '50', '100', '250', '500', '1000', '5000']

    sort_by, sort_order = list_sort(request)
    movie_list = Douban.objects.order_by(sort_by)
    # Export file code
    try:
        start_index = request.GET['start_index']
        end_index = request.GET['end_index']
    except KeyError:
        pass
    else:
        if end_index not in rows_num_list or start_index > end_index:
            return redirect('export_page')
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
            return redirect('export_page')
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
    total = movie_list.count()
    return render(request, 'export.html', context=locals())


@login_required
def settings_page(request):
    user_data = {}
    path = request.get_full_path()
    user_model = get_user_model()
    form = UserProfileChangeForm()
    # print(dir(request.user))
    if 'status' in request.GET:
        status = request.GET['status']
        return render(request, 'settings.html', {'status': status})
    if request.method == "POST":
        user_data['email'] = request.POST['email']
        user_data['real_name'] = request.POST['real_name']
        user_data['sex'] = request.POST['sex']
        user_data['phone_num'] = request.POST['phone_num']
        user_model.objects.filter(username=request.POST['username']).update(**user_data)
        return HttpResponseRedirect('?status=0')
    return render(request, 'settings.html', locals())


@login_required
def views_page(request):
    search_mode = True
    m_types = M_TYPES
    regions = REGIONS
    try:
        m_type = request.GET['m_type']
        keywords = request.GET['keywords']
        region = request.GET['region']
    except KeyError:
        movie_list = Douban.objects.all().order_by('-rate')
        search_mode = False
    else:
        movie_list = Douban.objects.filter((Q(title__icontains=keywords) | Q(director__icontains=keywords) |
                                            Q(scriptwriter__icontains=keywords) | Q(protagonist__icontains=keywords)) &
                                           Q(m_type__icontains=m_type) & Q(region__icontains=region)).order_by('-rate')
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
        total = movie_list.count()
        return render(request, 'views_search_page.html', context=locals())
    return render(request, 'views_page.html', context=locals())


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        validate_code = random_code(6)
        send_mail(
            'Password Validate Code',
            'Validate Code: %s' % validate_code,
            'from@example.com',
            [email],
            fail_silently=False,
        )
    return render(request, 'forgot_password.html')
