import json

from django.core import serializers

from bs4 import BeautifulSoup


def result(message, code, count, data):
    if count is None:
        count = 0
    if message == 1:
        message = 'success'
    elif message == 0:
        message = 'error'
    else:
        message = 'message error'

    result = {'code': code, 'msg': message, 'count': count, 'data': data}  # 自定义字符串格式

    # result['data'] = serializers.serialize('python', queryset=data)   #将data序列化

    return result


def getdatetime(date):
    dt_obj_without_ms = date.replace(microsecond=0)
    return dt_obj_without_ms  # 输出: "2024年07月01日 16：14：00"

def getdate(date):
     data=date.strftime('%Y年%m月%d日')
     return data


#剔除html只保留文本
def remove_html_tags(text):
    """
    This function takes a string that may contain HTML tags
    and returns a string with all HTML tags removed.
    """
    soup = BeautifulSoup(text, "html.parser")
    stripped_text = soup.get_text()
    return stripped_text


#剔除html中background属性
def remove_background_styles(html):
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html, 'html.parser')

    # 查找所有具有style属性的标签
    for tag in soup.find_all(style=True):
        # 如果style属性包含background相关设置，移除这部分
        if 'background' in tag['style']:
            # 分割style属性值，移除包含background的部分，再重新拼接
            style_parts = tag['style'].split(';')
            tag['style'] = ';'.join(filter(lambda p: not p.strip().startswith('background'), style_parts))
            # 确保去除连续的分号
            tag['style'] = tag['style'].replace(';;', ';').strip(';')

    # 返回处理后的HTML
    return str(soup)