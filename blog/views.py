# -*- coding:utf-8 -*-
from django.shortcuts import render,render_to_response

# Create your views here.
from blog.models import Blog,Tag, Author
from django.http import HttpResponse, Http404, HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import django_comments

def index(request):
    blogs = Blog.objects.all()
    tags = Tag.objects.all()
    paginator = Paginator(blogs,3)                                               #每页显示3篇blog进行分页
    page = request.GET.get('page')                                               #获取当前页的数字
    try:
     current_page = paginator.page(page)                                      #获取当前页
    except PageNotAnInteger:                                                     #如果系统从0开始，就赋初值为1
     current_page = paginator.page(1)
    blog_list = current_page.object_list                                         #获得当前页的blog

    return render_to_response('index.html',{'blogs':blogs,
                                         'tags': tags,
                                         'current_page':current_page})

def detail(request,id):                                             #参数由url传过来
    try:
        blog = Blog.objects.get(id=id)                              #检查该博客是否存在
    except Blog.DoesNotExist:
        raise Http404
    return render_to_response('detail.html',{'blog':blog})          #返回一个单独博客页面

def post(request):                                                    #跳转到post.html，这一步可以直接在前端实现
    return render_to_response('post.html')

def blog_add(request):
    content = request.POST.get('content')                             #在前端通过POST发送content数据给后台
    author = Author.objects.get(name='terry')                         #作者暂定为terry,以后可以根据实际登录人作为作者
    title = request.POST.get('title')                                 #在前端通过POST发送title数据给后台
    tag_name = request.POST.get('tags')                               #在前端通过POST发送tags数据给后台
    tag_name_string= request.POST.get('tags')                         #tag_name字符串是我们输入的一串tags以逗号隔开
    tag_name_list = tag_name_string.split(',')                        #通过split函数据所有的tag分装在列表中
    tags = Tag.objects.all()                                          #原先就有的tags
    for tag_name in tag_name_list:                                    #双重循环做的是如果输入的一串标签中原先没有的，就新建一个标签
     for tag in tags:
         if tag_name==tag.tag_name:
             break
     else:
         Tag.objects.create(tag_name=tag_name)
    blog=Blog.objects.create(title=title,                             #新建博客写入数据库中
                     author=author,
                     content=content,
                     )
    for tag_name in tag_name_list:
     blog.tags.add(Tag.objects.get(tag_name=tag_name))             #给博客加入标签

    id= Blog.objects.order_by('-date_time')[0].id                     #查找最新文章的id
    return HttpResponseRedirect('/blog/%s' %id)                       #数据输入到数据库这是后台做的事，前端显示该博客的单篇博客详细内容比较合适

#uploadImg
def mkdir(path):                                         #路径初始化，如果没有存放地点就新建
  path = path.strip()
  path = path.rstrip("\\")
  if not os.path.exists(path):
      os.makedirs(path)
  return path

def save_file(path, file_name, data):                   #把data保存path/file_name文件中
  if data == None:
      return
  mkdir(path)
  if(not path.endswith("/")):
      path=path+"/"
  file = open(path+file_name,"wb")
  file.write(data)
  file.flush()

def uploadImg(request):
  if request.method=='POST':
      file_obj = open("log.txt","w+")
      buf = request.FILES.get('file',None)                                    #获取的图片文件
      print >> file_obj, str(buf)
      file_buff = buf.read()                                                  #获取图片内容
      time_format=str(time.strftime("%Y-%m-%d-%H%M%S",time.localtime()))
      file_name = "img"+time_format+".jpg"                                    #img2016-02-13-072459.jpg
      save_file("blog/static/image", file_name,file_buff)                     #blog/static/image/img2016-02-13-072459.jpg
      dict_tmp = {}                                                           #kindeditor定义了返回的方式是json，
      dict_tmp['error']=0                                                     #成功{ "error":0, "url": "/static/image/filename"}
      dict_tmp['url']="/static/image/"+file_name
      return HttpResponse(json.dumps(dict_tmp))

def sub_comment(request):
    blog_id = request.POST.get('blog_id')                                #django_comments表中需要blog_id参数
    comment=request.POST.get('comment_content')
    django_comments.models.Comment.objects.create(
     content_type_id=9,                                               #content_type_id=9代表的是博客，8代表tag
     object_pk=blog_id,
     site_id=1,
     user=request.user,                                               #当前登录的用户
     comment=comment,
    )
    return HttpResponseRedirect('/blog/%s' %blog_id)

def tag_blog(request,id):
    tag = Tag.objects.get(id=id)                                        #根据id获取当前tag
    blogs = tag.blog_set.all()                                          #由于tag与blog是多对多关系，可以根据tag查找相应的blog
    paginator = Paginator(blogs,3)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    blog_list = current_page.object_list
    return render_to_response('index.html',{'blog_list':blog_list,
                                         'tag': tag,
                                         'current_page':current_page})