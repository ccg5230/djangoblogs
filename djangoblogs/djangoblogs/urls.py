"""djangoblogs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.contrib.sitemaps import views as sitemap_views

from blogs.views import post_list, post_detail
from blogs.views import (
    IndexView, CategoryView, TagView,
    PostDetailView,SearchView,
    AuthorView,
)
from blogs.rss import LatestPostFeed
from blogs.sitemap import PostSitemap

from config.views import LinkListView
from .custom_site import custom_site
from comment.views import CommentView

urlpatterns = [

    #使用funciton view方式
    #url(r'^$',post_list, name='index'),
    #url(r'^category/(?P<category_id>\d+)/$', post_list, name='category-list'),
    #url(r'tag/(?P<tag_id>\d+)/$', post_list, name='tag-list'),
    #url(r'^post/(?P<post_id>\d+).html$', post_detail, name='post-detail'),

    #使用 class-based-view
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category-list'),
    url(r'tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag-list'),
    url(r'^post/(?P<post_id>\d+).html$', PostDetailView.as_view(), name='post-detail'),
    url(r'^links/$', LinkListView.as_view(), name='links'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^author/(?P<owner_id>\d+)/$', AuthorView.as_view(), name='author'),
    url(r'^comment/$', CommentView.as_view(), name='comment'),
    url(r'^rss|feed/', LatestPostFeed(), name='rss'),
    url(r'^sitemap\.xml$', sitemap_views.sitemap, {'sitemaps': {'posts': PostSitemap}}),
    url(r'^super_admin/', admin.site.urls, name='super-admin'),
    url(r'^admin/', custom_site.urls, name='admin'),
]
