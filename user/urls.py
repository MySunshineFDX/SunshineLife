from django.urls import path

from . import views

# user模块的路由

app_name = 'user'  # 一定要指定命名空间

urlpatterns = [
    #用户
    path('index', views.index, name='user_index'),
    path('login', views.user_login, name='user_login'),
    path('register', views.register, name='user_register'),
    path('userupdate', views.userUpdate, name='user_update'),

    #类型
    path('gettype', views.getType, name='user_gettype'),
    path('addtype', views.addType, name='user_addtype'),
    path('alltype', views.allType, name='user_alltype'),
    path('updatetype', views.updateType, name='user_updatetype'),
    path('updatetypestu', views.updateTypeStu, name='user_updatetypestu'),


    #文章

    path('getessay', views.getEssay, name='user_getessay'),
    path('addessay', views.addEssay, name='user_addessay'),
    path('allessay', views.allEssay, name='user_allessay'),
    path('updateessay', views.updateEssay, name='user_updateessay'),
    path('updateessaystu', views.updateEssayStu, name='user_updateessaystu'),

    #公告
    path('getside', views.getSide, name='user_getside'),
    path('addside', views.addSide, name='user_addside'),
    path('allside', views.allSide, name='user_allside'),

    # 类型
    path('gettree', views.getTree, name='user_gettree'),
    path('addtree', views.addTree, name='user_addtree'),
    path('alltree', views.allTree, name='user_alltree'),
    path('updatetree', views.updateTree, name='user_updatetree'),
    path('updatetreestu', views.updateTreeStu, name='user_updatetreestu'),

    # path('url', views.url, name='user_login'),
    # path('add', views.user_add, name='user_add'),
    # path('query',views.user_query,name='user_query'),
    # path('update', views.user_update, name='user_update'),
    # path('delete', views.user_delete, name='user_del')
]
