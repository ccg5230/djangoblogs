from django.http import HttpResponse
from django.shortcuts import render
from .models import Post, Tag, Category
from config.models import SideBar


def post_list(request, category_id=None, tag_id=None):
    tag = None
    category = None

    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_posts()

    context = {
        'category': category,
        'tag': tag,
        'post_list': post_list,
        'sidebars': SideBar.get_all()
    }
    context.update(Category.get_navs(request))
    return render(request, 'blogs/list.html', context=context)


def post_detail(request, post_id=None):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None

    context = {
        'post': post,
        'sidebars': SideBar.get_all(),
    }

    return render(request, 'blogs/detail.html', context=context)
    #return HttpResponse('detail')

'''
使用class-based-view简化代码
'''
from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404

#基础数据视图
class CommentViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all(),
        })
        #self.request获取request
        context.update(Category.get_navs(self.request))
        return context

class IndexView(CommentViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list' #django封装了获取数据的代码
    template_name = 'blogs/list.html'

#分类列表
class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        '''重写queryset,根据分类过滤'''
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)

#标签列表
class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        '''重写queryset,根据标签过滤'''
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag_id=tag_id)

#文章详情页
class PostDetailView(CommentViewMixin, DetailView):
    queryset = Post.latest_posts()
    template_name = 'blogs/detail.html'
    context_object_name = 'post' #如果不设置此项，在template中需要使用object变量
    '''
    DetailView会根据pk去查询对象，不设置报错
    Generic detail view PostDetailView must be called with either an object pk or a slug in the URLconf.
    '''
    pk_url_kwarg = 'post_id'