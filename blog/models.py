# -*- coding:utf-8 -*-
from django.db import models

# Create your models here.

class Author(models.Model):                                          #作者信息
  """docstring for Author"""
  name = models.CharField(max_length=30)
  email = models.EmailField(blank=True)
  website = models.URLField(blank=True)

  def __unicode__(self):                                           #方便查询时返回一个名字，否则是一个实例
      return self.name

class Tag(models.Model):                                             #标签
  """tag of book"""
  tag_name = models.CharField(max_length = 30)
  create_time = models.DateTimeField(auto_now_add =True )

  def __unicode__(self):
      return self.tag_name

class Blog(models.Model):                                            #博客
  title = models.CharField(max_length=50)                          #标题
  author = models.ForeignKey(Author)                               #作者 作者与博客是一对多的关系，一个博客只有一个作者，一个作者可以有多个博客
  tags = models.ManyToManyField(Tag, blank=True)                   #标签 标签与博客是多对多的关系，一个博客有多个标签，一个标签也可以有多个博客，因此初始化时不能直接赋值，它是一个列表
  content = models.TextField()                                     #内容
  date_time = models.DateTimeField(auto_now_add = True)

  def __unicode__(self):
      return self.title

  class Meta:
      ordering = ['-date_time']                                    #按照时间排序