"""rogse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'detail/(?P<page>\d+)$', views.detail),
    url(r'next_detail/$', views.next_detail),
    url(r'movie_form/$', views.movie_form),
    url(r'home/$', views.home),
    url(r'^listing/$', views.listing),
    url(r'^login/$', views.login_page, name='login_page'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^register/$', views.register, name='register'),
    url(r'^settings/$', views.settings_page, name='settings_page'),
    url(r'^reports/$', views.reports_page, name='reports_page'),
    url(r'^analytics/$', views.analytics_page, name='analytics_page'),
    url(r'^export/$', views.export_page, name='export_page'),
    url(r'^views/$', views.views_page, name='views_page'),
    url(r'^forgotpassword/$', views.forgot_password, name='forgot_password'),
]
