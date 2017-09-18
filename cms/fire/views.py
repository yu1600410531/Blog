# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect,reverse,get_object_or_404,HttpResponse,HttpResponseRedirect
from models import Article,Comment,Poll,NewUser,Column,Author
from forms import LoginForm,SearchForm,SetInfoForm,RegisterForm,CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import markdown2, urlparse
from django.db.models import Q
# Create your views here.
from django.core.paginator import PageNotAnInteger,EmptyPage,InvalidPage,Paginator
import uuid
import os
from cms import settings

# 下载保存图片
def upload_avatar(file):
    file_type = file.content_type
    file_name = file.name
    file_size = file.size
    file_type_list = ['image/jpeg','image/gif', 'image/jpg']
    # if file_size /1024/1024 < 2:
    if file_type in file_type_list:
        # 生成唯一不重复name,
        uname = str(uuid.uuid4()) + '.jpg'

        # 绝对路径,文件路径
        filepath = os.path.join(settings.BASE_DIR, 'upload') + '/user/' + uname

        # 数据库中存在的路径
        dbpath = 'user/' + uname

        # 文件是否过大，大于2.5M标准
        if file.multiple_chunks():
            with open(filepath, 'wb') as f:
                # 分解文件
                for chunk in file.chunks():
                    f.write(chunk)
        else:
            # 正常大小状况
            with open(filepath, 'wb') as f:
                file_content = file.read()
                f.write(file_content)
        return True, '上传成功',dbpath
    else:
        return  False,'文件格式不正确！'

# 主页
def index(request):
    latest_article_list = Article.objects.query_by_time()
    loginform = LoginForm()
    column_list = Column.objects.all()
    pn = request.GET.get('pn', 1)
    article_list, number_pages, number,pn = cut_page(pn, latest_article_list)

    # print column_list
    context = {
        'latest_article_list': article_list,
        'login_form': loginform,
        'column_list': column_list,
        'numbers': number,
        'num_pages': number_pages,
        'pn': pn,
        'temp_list':article_list
    }
    return render(request,'index.html', context)

# 搜索文章
def search(request):

    search_word = request.GET.get('search_word')
    if search_word is not None and search_word != '':
        conditon = Q(title__icontains=search_word) | Q(author__name__icontains=search_word) | Q(column__name__icontains=search_word)
        article_list = Article.objects.filter(conditon).all()
        pn = request.GET.get('pn', 1)
        article_list, number_pages, number, pn = cut_page(pn, article_list)
        # return HttpResponse('OK')
        context = {
            'article_list': article_list,
            'numbers': number,
            'num_pages': number_pages,
            'pn': pn,
            'temp_list':article_list,
        }
        if article_list:
            return render(request,'column_article.html', context)
        else:
            return render(request, 'column_article.html', {'msg': '未能搜索结果！'})
    else:
        return render(request,'column_article.html', {'msg':'未能搜索结果！'})


# 分页单独提取出来，通用
def cut_page(pn,obj):
    try:
        pn = int(pn)
    except Exception as e:
        print str(e)
        pn = 1
    pagi = Paginator(obj, 6)
    # 获取某一页记录
    try:
        temp_list = pagi.page(pn)
    except (PageNotAnInteger, EmptyPage, InvalidPage) as e:
        print str(e)
        pn = 1
        temp_list = pagi.page(pn)
    number_pages = temp_list.paginator.num_pages
    if number_pages is None:
        # 判断pn是否超标，过大或过小
        number_pages = 0
    if pn > number_pages:
        pn = number_pages
    elif pn < 1:
        pn = 1

        #     判断下方小格子的起始和结束
    if number_pages > 5:
        if pn >= number_pages - 2:
            start = number_pages - 4
            end = number_pages + 1
        elif pn <= 2:
            start = 1
            end = 6
        else:
            start = pn - 2
            end = pn + 3
    else:
        start = 1
        end = number_pages + 1
    number = range(start, end)

    return temp_list, number_pages, number, pn

# 登录
def log_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form':form})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['uid']
            password = form.cleaned_data['pwd']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                url = request.POST.get('source_url', '/fire')
                return  redirect(url)
            else:
                return render(request, 'login.html', {'form':form, 'error':'password or username is not true!'})
        else:
            return render(request,'login.html', {'form':form})

@login_required
def log_out(request):
    url = request.POST.get('source_url', '/fire/')
    # url = reverse('')
    print url
    logout(request)
    return redirect(url)

# 查看某一篇文章
def article(request, article_id):
    # 可以直接通过输入url来访问当页面不存在时，我们就要进行相关处理
    article_id = int(article_id)
    article = get_object_or_404(Article,id=article_id)
    # django可以集成各种富文本编辑器，还有ueditor。markdown
    # content = markdown2.markdown(article.content,extras=['code-friendly','fenced-code-blocks',
    #                                                      'header-ids','toc', 'metadata'])
    content = article.content
    commentform = CommentForm()
    loginform = LoginForm()
    comments = article.comment_set.all()

    return render(request, 'article_page.html',{
        'article':article,
        'loginform':loginform,
        'commentform':commentform,
        'content':content,
        'comments':comments,
    })

# 文章评论
@login_required
def comment(request, article_id):
    form = CommentForm(request.POST)
    url = urlparse.urljoin('/fire/', article_id)
    if form.is_valid():
        user = request.user
        article = Article.objects.get(id=article_id)
        new_commnet = form.cleaned_data['comment']
        c = Comment(content=new_commnet, article_id=article_id)
        c.user = user
        c.save()
        article.comment_num += 1
    return redirect(url)

# 文章收藏
@login_required
def get_keep(request, article_id):
    logged_user = request.user
    article = Article.objects.get(id=article_id)
    articles = logged_user.article_set.all()
    if article not in articles:
        article.user.add(logged_user)
        article.keep_num += 1
        article.save()
        return redirect('/fire/')
    else:
        url = urlparse.urljoin('/fire/', article_id)
        return redirect(url)

# 文章点赞
@login_required
def get_poll_article(request, article_id):
    logged_user = request.user
    article = Article.objects.get(id=article_id)
    polls = logged_user.poll_set.all()
    articles =[]
    for poll in polls:
        articles.append(poll.article)

    if article in articles:
        url = urlparse.urljoin('/fire/', article_id)
        return redirect(url)
    else:
        article.poll_num += 1
        article.save()
        poll = Poll(user=logged_user, article=article)
        poll.save()
        data ={}
        return redirect('/fire/')

# 注册
def register(request):
    error1 = '用户名已存在！'
    valid = "用户名可用！"

    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'register.html', {'form':form})
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        # # 一种是用户ajax请求，一个时用户提交的请求
        # if request.POST.get('raw_username','erjgiqfv240hqp5668ej23foi') != 'erjgiqfv240hqp5668ej23foi':
        #     try:
        #         print request.POST.get('raw_username', '')
        #         user = NewUser.objects.get(username=request.POST.get('raw_username', ''))
        #     except ObjectDoesNotExist:
        #         return render(request, 'register.html', {'form':form, 'msg':'用户名已被使用，请更换！'})
        #     else:
        #         return render(request, 'register.html', {'form': form, 'msg': '用户名可以使用！'})
        # else:
        # if form.is_valid():
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        profile = request.POST.get('profile')
        avatar = request.FILES.get('avatar')
        print username,email,password1,password2,profile,avatar
        res = upload_avatar(avatar)
        try:
                # print request.POST.get('raw_username', '')
            user = NewUser.objects.get(username=username)
            if user:
                return render(request, 'register.html', {'form': form, 'msg': '用户名已被使用，请更换！'})
        except ObjectDoesNotExist:
            if password1 == password2 and res[0]:
                user_info = {
                    'username':username,
                    'email':email,
                    'password':make_password(password1),
                    'profile':profile,
                    'avatar':res[2],
                }
                user = NewUser(**user_info)
                user.save()
                return redirect('/fire/login')
            else:
                return render(request, 'register.html', {'form': form, 'msg': '服务器繁忙，请重试！'})
        # else:
        #     return render(request, 'register.html', {'form':form,'msg': '输入不能为空！'})

# 修改用户信息
@login_required
def modify_user(request):
    column_list = Column.objects.all()
    if request.method == 'GET':
        return render(request, 'modify_user.html',{'column_list':column_list})
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        profile = request.POST.get('profile')
        print username,email,profile
        try:
            avatar = request.FILES.get('avatar')
            res = upload_avatar(avatar)
            if res[0]:
                avatar_path = res[2]
            else:
                error = res[1]
                avatar_path = request.user.avatar
        except:
            avatar_path = request.user.avatar
        user_info = {
            'username': username,
            'email': email,
            'profile': profile,
            'avatar': avatar_path,
        }
        try:
            NewUser.objects.filter(id=request.user.id).update(**user_info)
            user = NewUser.objects.get(id=request.user.id)
            user.save()

            return redirect(reverse('fire:user_detail'))
        except:
            return redirect(reverse('fire:modify_user'))


# 获取分类文章
def get_column(request, column_id):
    column = get_object_or_404(Column, id=column_id)
    article_list = column.article_set.all()
    pn = request.GET.get('pn', 1)
    temp_list, number_pages, number, pn = cut_page(pn, article_list)
    context = {
        'temp_list': temp_list,
        'numbers': number,
        'num_pages': number_pages,
        'pn': pn,
    }
    return render(request, 'column_article.html', context)

# 用户信息
@login_required
def user_detail(request):
    column_list = Column.objects.all()[0:5]
    logged_user = request.user
    return render(request, 'user_detail.html', {'user':logged_user, 'column_list':column_list})

# 编写文章
# @login_required
# def create_article(request):
#     column_list = Column.objects.all()
#     if request.method == 'GET':
#
#         return render(request, 'create_article.html', {'column_list':column_list})
#     if request.method =='POST':
#         column_id = request.POST.get('column')
#         title = request.POST.get('title')
#         content = request.POST.get('content')
#
#         author_name =  request.POST.get('author_name')
#         profile =  request.POST.get('profile')
#         password1 =  request.POST.get('password1')
#         password2 =  request.POST.get('password2')
#
#         try:
#             author = Author.objects.get(name=author_name)
#             # return render(reverse('fire:create_article', kwargs={'msg':'作者 '}))
#         except ObjectDoesNotExist:
#             if password1 == password1:
#                 try:
#                     author_info = {
#                         'name':author_name,
#                         'profile':profile,
#                         'password':password1,
#                     }
#                     author = Author.objects.create(**author_info)
#                     author.save()
#                 except Exception as e:
#                     print str(e)
#                     # return redirect(reverse('fire:create_article', kwargs={}))
#                     return render(request, 'create_article.html', {'column_list': column_list,'msg':'服务器错误，作者添加失败'})
#             else:
#                 # return redirect(reverse('fire:create_article', kwargs={'msg': '密码输入不一致'}))
#                 return render(request, 'create_article.html', {'column_list': column_list, 'msg': '密码输入不一致'})
#
#         article_info = {
#             'column_id': column_id,
#             'title':title,
#             'content':content,
#             'author_id':author.id,
#         }
#         try:
#             article = Article.objects.create(**article_info)
#             article.save()
#             return redirect(reverse('fire:article', kwargs={'article_id':article.id}))
#         except Exception as e:
#             print str(e)
#             # return redirect(reverse('fire:create_article', kwargs={'msg': '服务器繁忙，文章保存失败！'}))
#             return render(request, 'create_article.html', {'column_list': column_list, 'msg': '服务器繁忙，文章保存失败！'})


@login_required
def create_article(request):
    column_list = Column.objects.all()
    author_list = Author.objects.all()
    if request.method == 'GET':
        return render(request, 'create_article.html', {'column_list': column_list, 'author_list':author_list})
    if request.method == 'POST':
        column_id = request.POST.get('column')
        title = request.POST.get('title')
        content = request.POST.get('content')
        author_id = request.POST.get('author_id')
        article_info = {
            'column_id': column_id,
            'title': title,
            'content': content,
            'author_id': author_id,
        }
        try:
            article = Article.objects.create(**article_info)
            article.save()
            return redirect(reverse('fire:article', kwargs={'article_id':article.id}))
        except Exception as e:
            print str(e)
            return render(request, 'create_article.html', {'column_list': column_list,'author_list':author_list, 'msg': '服务器繁忙，文章保存失败！'})


@login_required
def user_poll(request):
    user_poll_article = request.user.poll_set.all()
    pn = request.GET.get('pn', 1)
    if user_poll_article:
        temp_list, number_pages, number, pn = cut_page(pn, user_poll_article)
        context = {
            'temp_list': temp_list,
            'numbers': number,
            'num_pages': number_pages,
            'pn': pn,
        }
        return render(request, 'user_action_article.html',context)
    else:
        return render(request, 'user_action_article.html',{'msg':'您还没有点过赞的的文章！'} )


@login_required
def user_keep(request):
    user_keep_article = request.user.article_set.all()
    pn = request.GET.get('pn', 1)
    if user_keep_article:
        temp_list, number_pages, number, pn = cut_page(pn, user_keep_article)
        context = {
            'temp_list': temp_list,
            'numbers': number,
            'num_pages': number_pages,
            'pn': pn,
        }
        return render(request, 'column_article.html',context)
    else:
        return render(request, 'column_article.html',{'msg':'您还没有点过赞的的文章！'} )

@login_required
def user_comment(request):
    user_comment_article = request.user.comment_set.all()
    pn = request.GET.get('pn', 1)
    if user_comment_article:
        temp_list, number_pages, number, pn = cut_page(pn, user_comment_article)
        context = {
            'temp_list': temp_list,
            'numbers': number,
            'num_pages': number_pages,
            'pn': pn,
        }
        return render(request, 'user_action_article.html',context)
    else:
        return render(request, 'user_action_article.html',{'msg':'您还没有点过赞的的文章！'} )






