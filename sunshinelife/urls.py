"""
URL configuration for sunshinelife project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

    路径
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('user/', include("user.urls")),  # 导入user模块的路由

    path('', include("essay.urls"))   # 导入essay模块的路由

    # 登录路由查询字符的方式
    # path('user', user_view.login),
    # 登录路由在path中携带
    # 限制类型  int  str  slug uuid path
    # path('user/<int:user_id>/<user_name>', user_view.login_path)
]
