import datetime

from django.db import models
from django.forms import EmailField


# 默认生成主键 id
class UserMsg(models.Model):
    userid = models.CharField(max_length=30)  # 账号
    show = models.TextField(null=True, blank=True)  # 简介
    created = models.DateTimeField(auto_now_add=True)  # 创建时间
    updatetime = models.DateTimeField(auto_now=True)  # 修改时间
    remark = models.CharField(max_length=60, null=True, blank=True)  # 备注

    class Meta:
        db_table = 'user_msg'  # 设置表名