# -*- coding:utf-8 -*-
from django.contrib import admin

# Register your models here.
from blog.models import Author,Tag,Blog

class AuthorAdmin(admin.ModelAdmin):                     #定制Author界面
  list_display=('name','email','website')              #分为name,email,website三列进行显示
  search_field=('name')

class BlogAdmin(admin.ModelAdmin):                       #定制Blog界面
  list_display = ('title','author','date_time')
  list_filter = ('date_time',)                         #按照时间进行查看
  filter_horizontal=('tags',)                          #tag水平选择

admin.site.register(Author, AuthorAdmin)                 #注册
admin.site.register(Blog,BlogAdmin)
admin.site.register(Tag)