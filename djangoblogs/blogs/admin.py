from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from djangoblogs.base_admin import  BaseOwnerAdmin
from djangoblogs.custom_site import custom_site

#同一页面编辑关联数据
class PostInline(admin.TabularInline):  # StackedInline  样式不同
    fields = ('title', 'desc')
    extra = 1  # 控制额外多几个
    model = Post

@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline,]
    list_display = ('name', 'status', 'is_nav', 'owner', 'created_time') #列表显示字段
    fields = ('name', 'status', 'is_nav') #新增、编辑字段

    ''''#重写svae_model方法，设置owner
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)
        '''

@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
   list_display = ('name', 'status', 'owner', 'created_time')
   fields = ('name', 'status')


class CategoryOwnerFilter(admin.SimpleListFilter):
    '''自定义过滤器只展示当前用户分类'''

    title = '分类过滤器'
    parameter_name = 'owner_category' #查询时url参数名称：http://xxxx?owner_category=1

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id','name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post, site=custom_site)
#class PostAdmin(admin.ModelAdmin):
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm

    list_display = [
        'title', 'category', 'status', 'desc',
         'created_time', 'owner', 'operator',
    ]
    list_display_links = []

    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category__name']
    save_on_top = True

    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    save_on_top = True

    exclude = ['owner']
    '''
    fields = (
        ('category', 'title'),
        'desc',
        'status',
        'content',
        'tag'
    )'''
    #使用fieldsets配置字段展示
    ''''''
    fieldsets = (
        ('基础配置',{
           'description': '基础配置',
            'fields':(
                ('title', 'category'),
                'status'
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content'
            ),
        }),
        ('额外信息', {
            #collapse样式定义display: none;
            'classes': ( 'wide',),#元组只有一个元素需要加逗号，表明是元组
            'fields': ('tag',),
        })
    )

    #filter_horizontal = ('tags',) #水平展示多对多字段
    filter_vertical = ('tag',) #垂直展示多对多字段

    #列表增加编辑按钮
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blogs_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'

    class Media:
        '''
        测试
        #css样式引起删除按钮height=15px显示不全，要为35px
        css = {
            'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),
        }
        js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)'''

from django.contrib.admin.models import LogEntry


@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']
