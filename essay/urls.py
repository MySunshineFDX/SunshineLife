from django.urls import path

from . import views

# essay模块的路由

app_name = 'essay'  # 一定要指定命名空间

urlpatterns = [
    path('', views.index, name='index'),
    path('essayajax', views.essayajax, name='essayajax'),
    path('essaysearch',views.essaySearch, name='essaysearch'),
    path('getessay',views.getEssay, name='getessay'),
    path('timetree',views.timeTree, name='timetree')
]
