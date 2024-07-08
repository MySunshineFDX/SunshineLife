from django.db import models
import datetime


# Create your models here.
class essay_type(models.Model):  # 类型
    typeid = models.AutoField(primary_key=True)  # 类型id
    type = models.CharField(max_length=10, null=True)  # 类型名称
    created = models.DateTimeField(auto_now_add=True)  # 创建时间
    updatetime = models.DateTimeField(auto_now=True)  # 修改时间
    remark = models.CharField(max_length=60, null=True, blank=True)  # 备注
    status = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'essay_type'


class essay(models.Model):
    essayid = models.AutoField(primary_key=True)  # 文章id
    title = models.CharField(max_length=60, null=True)  # 文章标题
    content = models.TextField(null=True)  # 内容
    created = models.DateTimeField(auto_now_add=True)  # 创建时间
    updatetime = models.DateTimeField(auto_now=True)  # 修改时间
    remark = models.CharField(max_length=60, null=True, blank=True)  # 备注
    status = models.CharField(max_length=20, null=True, blank=True)
    typedata = models.ForeignKey("essay_type", on_delete=models.CASCADE)

    class Meta:
        db_table = 'essay'


class side(models.Model):
    message = models.TextField(null=True)

    class Meta:
        db_table = 'side'


class timeTree(models.Model):
    event = models.TextField(null=True)  # 事件
    created = models.DateTimeField(auto_now_add=True)  # 创建时间
    updatetime = models.DateTimeField(auto_now=True)  # 修改时间
    status = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'timetree'
