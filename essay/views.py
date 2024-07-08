from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from django.forms import model_to_dict
# Create your views here.
from .models import *
from .models import timeTree as  tt
from tool.Tool import *


# 初始方法
def index(request):
    if request.method == 'GET':  # 判断是否分类选择
        typeid = request.GET.get('typeid', None)
        request.session["typeid"] = typeid  # 向session中存储查typeid
        request.session["keywords"] = None  # 将关键词查询设为none
    # 文章类型检索
    all_type = essay_type.objects.filter(status=1)
    typedb = []
    for item in all_type:
        typedb.append({
            'typeid': item.typeid,
            'type': item.type,
        })
    # 公告检索
    sidedb = side.objects.order_by('-id')
    # 近期文章检索
    essaydb = essay.objects.filter(status=1).order_by('-created')[:6]
    recent = []
    for item in essaydb:
        recent.append({'title': item.title, 'essayid': item.essayid})

    context = {'typedb': typedb, 'message': sidedb[0].message, "recent": recent, 'essaydata': None}
    return render(request, 'index.html', context=context)


# 关键词查询文章
@require_http_methods(['GET', 'POST'])
def essaySearch(request):
    if request.method == 'GET':
        keywords = request.GET.get('keywords', None)  # 获取关键词
        request.session["keywords"] = keywords  # 存储关键词
        request.session["typeid"] = None  # 将类型查询的设为none

        # 文章类型检索
        all_type = essay_type.objects.filter(status=1)
        typedb = []
        for item in all_type:
            typedb.append({
                'typeid': item.typeid,
                'type': item.type,
            })
        # 公告检索
        sidedb = side.objects.order_by('-id')
        # 近期文章检索
        essaydb = essay.objects.filter(status=1).order_by('-created')[:6]
        recent = []
        for item in essaydb:
            recent.append({'title': item.title, 'essayid': item.essayid})

        context = {'typedb': typedb, 'message': sidedb[0].message, "recent": recent, 'essaydata': None}
        return render(request, 'index.html', context=context)


# 文章内容ajax处理
@require_http_methods(['GET', 'POST'])
def essayajax(request):
    typeid = request.session["typeid"]
    keywords = request.session["keywords"]
    if typeid is not None and keywords is None:  # 分类查询时
        essaydb = essay.objects.filter(status=1, typedata=typeid).order_by('-created')
    elif typeid is None and keywords is not None:  # 关键字查询时
        essaydb = essay.objects.filter(status=1, title__contains=keywords).order_by('-created')
    else:  # 默认查询
        essaydb = essay.objects.filter(status=1).order_by('-created')

    page = request.GET.get('page', 1)  # 获取页数
    paginator_data = Paginator(essaydb, 6).get_page(page)  # 设置获取的页数与数量 6
    total_pages = Paginator(essaydb, 6).num_pages  # 获取总页
    essaydata = []
    for item in paginator_data:
        date = getdate(item.created)
        content = remove_html_tags(item.content)
        essaydata.append({
            'createtime': date,
            'title': item.title,
            'essayid': item.essayid,
            'typedata': item.typedata.type,
            'content': content
        })
        # keywords = request.session["keywords"]
    context = result(1, 200, total_pages, essaydata)
    return JsonResponse(context, safe=False)


# 关键词查询文章
@require_http_methods(['GET', 'POST'])
def getEssay(request):
    if request.method == 'GET':
        essayid = request.GET.get('essayid')
        essaydb = essay.objects.get(essayid=essayid)
        date = getdate(essaydb.created)
        essaydata = []
        essaydata.append({
            'createtime': date,
            'title': essaydb.title,
            'essayid': essaydb.essayid,
            'typedata': essaydb.typedata.type,
            'content': essaydb.content
        })
        context = result(1, 200, 0, essaydata)
        return JsonResponse(context, safe=False)


#  时间树
@require_http_methods(['GET', 'POST'])
def timeTree(request):
    if request.method == 'GET':
        data = tt.objects.filter(status=1).order_by('-created')
        timeTreedata = []
        for item in data:
            date = getdate(item.created)
            timeTreedata.append({
                'createtime': date,
                'event': item.event,
            })
        context = result(1, 200, 0, timeTreedata)
        return JsonResponse(context, safe=False)
