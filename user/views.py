from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import HttpResponse, render, redirect
from django.urls.base import reverse_lazy

import time
from django.views.decorators.http import require_http_methods

from .form import *
from .models import UserMsg
from essay.models import essay, essay_type, side, timeTree  # 导入essay app 模型
from essay.form import *

from django.contrib.auth import get_user_model, login

from tool.Tool import *

Sys_User = get_user_model()


# 在url中携带参数
# 通过查询字符的方式（query string） http://127.0.0.1:8000/user?id=3&name=ppp
# 在path中携带  http://127.0.0.1:8000/user/2/hhh


# 用户主页
@login_required(login_url=reverse_lazy('user:user_login'))
def index(request):
    session_id = request.session["id"]  # 获取session中的id
    sys_user = Sys_User.objects.get(id=session_id)
    datatime = time.strftime("%Y年%m月%d日 %H:%M:00", time.localtime())
    context = {
        'name': sys_user.username,
        'time': datatime
    }
    return render(request, 'userIndex.html', context=context)


# 用户注册
@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        code = request.POST.get("code")
        if code != 'XXX420159':
            return HttpResponse("注册码有误")
        else:
            form = RegisterForm(request.POST)
            if form.is_valid():
                username = form.data.get("username")
                email = form.data.get("email")
                password = form.data.get("password")
                data_userid = Sys_User.objects.filter(email=email)
                if len(data_userid) != 0:
                    return HttpResponse("邮箱重复！")
                else:
                    Sys_User.objects.create_user(username=username, email=email, password=password)
                    # 检索出用户信息 储存在USERMSG表中
                    sys_user = Sys_User.objects.get(email=email, username=username)
                    UserMsg.objects.create(userid=sys_user.id)
                    context = {
                        'email': email,
                    }
                    return render(request, 'login.html', context=context)
            else:
                return HttpResponse("注册格式有误")


# 用户登陆验证逻辑
@require_http_methods(['GET', 'POST'])
def user_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            email = loginform.cleaned_data.get('email')
            password = loginform.cleaned_data.get('password')
            sys_user = Sys_User.objects.filter(email=email).first()
            if sys_user and sys_user.check_password(password):
                # 登录
                login(request, sys_user)
                request.session["id"] = sys_user.id  # 向session中存储用户唯一键
                # 过期时间直接设置为零
                request.session.set_expiry(0)
                return redirect('user:user_index')
            else:
                return HttpResponse("验证失败")
        else:
            return HttpResponse("数据有误")


# 修改个人信息
@login_required(login_url=reverse_lazy('user:user_login'))
@require_http_methods(['GET', 'POST'])
def userUpdate(request):
    if request.method == 'GET':  # 通过get方法获取用户的基本信息回填表填
        session_id = request.session["id"]
        user = UserMsg.objects.get(userid=session_id)
        sys_user = Sys_User.objects.get(id=session_id)
        context = {'username': sys_user.username, 'show': user.show}  # 信息拼接
        return render(request, 'userUpdate.html', context=context)
    else:
        session_id = request.session["id"]  # 获取session中的id
        # 保存
        show = request.POST.get('show')
        user = UserMsg.objects.get(userid=session_id)
        user.show = show
        user.save()
        username = request.POST.get('username')
        sys_user = Sys_User.objects.get(id=session_id)
        sys_user.username = username
        sys_user.save()
        context = {'username': sys_user.username, 'show': user.show}
        return render(request, 'userUpdate.html', context=context)


# 文章类型页面
@login_required(login_url=reverse_lazy('user:user_login'))
@require_http_methods(['GET', 'POST'])
def getType(request):
    return render(request, 'allType.html')


# 查看全部类型
@login_required(login_url=reverse_lazy('user:user_login'))
@require_http_methods(['GET', 'POST'])
def allType(request):
    if request.method == 'GET':
        all_type = essay_type.objects.all()
        json = []
        for item in all_type:
            item.status = '启用' if item.status == '1' else '禁用'
            json.append({
                'typeid': item.typeid,
                'type': item.type,
                'remark': item.remark,
                'status': item.status
            })
        context = result(1, 200, all_type.count(), json)
        return JsonResponse(context, safe=False)


# 添加类型
@login_required(login_url=reverse_lazy('user:user_login'))
@require_http_methods(['POST'])
def addType(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        essay_type(type=type, status=1).save()  # 保存的类型并启用
        return redirect('user:user_gettype')  # 返回表格界面


# 编辑类型
@login_required(login_url=reverse_lazy('user:user_login'))
@require_http_methods(['POST'])
def updateType(request):
    if request.method == 'POST':
        typeid = request.POST.get('typeid')
        type = request.POST.get('type')
        remark = request.POST.get('remark')
        data = essay_type.objects.get(typeid=typeid)
        data.type = type
        data.remark = remark
        data.save()
        return redirect('user:user_gettype')  # 返回表格界面


# 类型状态变更
@login_required(login_url=reverse_lazy('user:user_login'))
@require_http_methods(['GET'])
def updateTypeStu(request):
    if request.method == 'GET':
        typeid = request.GET.get('typeid')
        data = essay_type.objects.get(typeid=typeid)  # 根据数据库的状态值去改变
        # print(data.status)
        if data.status == '1' or data.status == 1:
            data.status = 0
        else:
            data.status = 1
        data.save()
        return redirect('user:user_gettype')  # 返回表格界面


# 文章页面
@login_required(login_url=reverse_lazy('user:user_login'))
@require_http_methods(['GET', 'POST'])
def getEssay(request):
    return render(request, 'allEssay.html')


# 查看文章全部
@login_required(login_url=reverse_lazy('user:user_login'))
@require_http_methods(['GET', 'POST'])
def allEssay(request):
    if request.method == 'GET':
        all_type = essay.objects.all().order_by('-created')
        json = []
        for item in all_type:
            item.status = '启用' if item.status == '1' else '禁用'
            item.created = getdatetime(item.created)
            json.append({
                'essayid': item.essayid,
                'typeid': item.typedata.typeid,
                'type': item.typedata.type,
                'title': item.title,
                'content': item.content,
                'created': item.created,
                'remark': item.remark,
                'status': item.status
            })
        context = result(1, 200, all_type.count(), json)
        return JsonResponse(context, safe=False)


# 新增文章
@login_required(login_url=reverse_lazy('user:user_login'))
@require_http_methods(['GET', 'POST'])
def addEssay(request):
    if request.method == 'GET':
        all_type = essay_type.objects.filter(status=1)
        data = []
        for item in all_type:
            data.append({
                'typeid': item.typeid,
                'type': item.type,
            })
        context = {"data": data}
        return render(request, 'addEssay.html', context=context)
    else:
        typeid = request.POST.get('typeid')
        type = essay_type.objects.get(typeid=typeid)  # 类型对象
        title = request.POST.get('title')
        content = request.POST.get('content')
        content_dispose = remove_background_styles(content)
        remark = request.POST.get('remark')

        essay.objects.create(typedata=type, title=title, content=content_dispose, remark=remark, status=1).save()
        return redirect('user:user_getessay')


# 文章状态变更
@login_required(login_url=reverse_lazy('user:user_login'))
@require_http_methods(['GET'])
def updateEssayStu(request):
    if request.method == 'GET':
        essayid = request.GET.get('essayid')
        data = essay.objects.get(essayid=essayid)  # 根据数据库的状态值去改变
        # print(data.status)
        if data.status == '1' or data.status == 1:
            data.status = 0
        else:
            data.status = 1
        data.save()
        return redirect('user:user_getessay')  # 返回表格界面


# 编辑文章
@login_required(login_url=reverse_lazy('user:user_login'))
@require_http_methods(['GET', 'POST'])
def updateEssay(request):
    if request.method == 'GET':
        # 获取文章类型
        all_type = essay_type.objects.filter(status=1)
        typedb = []
        for item in all_type:
            typedb.append({
                'typeid': item.typeid,
                'type': item.type,
            })
        essayid = request.GET.get('essayid')
        data = essay.objects.get(essayid=essayid)

        context = {"typedb": typedb,
                   "essayid": essayid,
                   "title": data.title,
                   "typeid": data.typedata.typeid,
                   "content": data.content,
                   "remark": data.remark,
                   }
        return render(request, 'updateEssay.html', context=context)
    else:
        typeid = request.POST.get('typeid')
        type_data = essay_type.objects.get(typeid=typeid)
        essayid = request.POST.get('essayid')
        title = request.POST.get('title')
        content = request.POST.get('content')
        content_dispose = remove_background_styles(content)
        remark = request.POST.get('remark')
        data = essay.objects.get(essayid=essayid)
        data.title = title
        data.content = content_dispose
        data.remark = remark
        data.typedata = type_data
        data.save()
        return redirect('user:user_getessay')  # 返回表格界面


# 公告页面
@login_required(login_url=reverse_lazy('user:user_login'))
@require_http_methods(['GET', 'POST'])
def getSide(request):
    return render(request, 'allSide.html')


# 查看公告
@login_required(login_url=reverse_lazy('user:user_login'))
@require_http_methods(['GET', 'POST'])
def allSide(request):
    if request.method == 'GET':
        data = side.objects.order_by('-id')
        json = []
        for i in data:
            json.append({
                'id': i.id,
                'message': i.message
            })
    context = result(1, 200, None, json)
    return JsonResponse(context, safe=False)


# 添加公告
@login_required(login_url=reverse_lazy('user:user_login'))
@require_http_methods(['POST'])
def addSide(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        side(message=message).save()  # 保存的类型并启用
        return redirect('user:user_getside')  # 返回表格界面


# 编辑公告
@login_required(login_url=reverse_lazy('user:user_login'))
@require_http_methods(['POST'])
def updateSide(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        message = request.POST.get('message')
        data = side.objects.get(id=id)
        data.message = message
        data.save()
        return redirect('user:user_getside')  # 返回表格界面


# 时间树页面
@login_required(login_url=reverse_lazy('user:user_login'))
@require_http_methods(['GET', 'POST'])
def getTree(request):
    return render(request, 'allTimeTree.html')


# 查看全部时间树
@login_required(login_url=reverse_lazy('user:user_login'))
@require_http_methods(['GET', 'POST'])
def allTree(request):
    if request.method == 'GET':
        all_timeTree = timeTree.objects.all()
        json = []
        for item in all_timeTree:
            item.status = '启用' if item.status == '1' else '禁用'
            created = getdate(item.created)
            json.append({
                'id': item.id,
                'created': created,
                'event': item.event,
                'status': item.status
            })
        context = result(1, 200, None, json)
        return JsonResponse(context, safe=False)


# 添加时间树
@login_required(login_url=reverse_lazy('user:user_login'))
@require_http_methods(['POST'])
def addTree(request):
    if request.method == 'POST':
        event = request.POST.get('event')
        timeTree(event=event, status=1).save()  # 保存的类型并启用
        return redirect('user:user_gettree')  # 返回表格界面


# 编辑时间树
@login_required(login_url=reverse_lazy('user:user_login'))
@require_http_methods(['POST'])
def updateTree(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        event = request.POST.get('event')
        data = timeTree.objects.get(id=id)
        data.event = event
        data.save()
        return redirect('user:user_gettree')  # 返回表格界面


# 时间树状态变更
@login_required(login_url=reverse_lazy('user:user_login'))
@require_http_methods(['GET'])
def updateTreeStu(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        data = timeTree.objects.get(id=id)  # 根据数据库的状态值去改变
        if data.status == '1' or data.status == 1:
            data.status = 0
        else:
            data.status = 1
        data.save()
        return redirect('user:user_gettype')  # 返回表格界面
