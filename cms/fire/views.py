# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect,reverse,get_object_or_404,HttpResponse,HttpResponseRedirect
from models import Article,Comment,Poll,NewUser,Column
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



def index(request):
    latest_article_list = Article.objects.query_by_time()
    loginform = LoginForm()
    column_list = Column.objects.all()[0:5]
    # print column_list
    context = {
        'latest_article_list':latest_article_list,
        'login_form':loginform,
        'column_list':column_list
    }
    return render(request,'index.html', context)

def search(request):
    if request.method == 'POST':
        search_word = request.POST.get('search_word')
        if search_word is not None and search_word != '':
            conditon = Q(title__icontains=search_word) | Q(author__name__icontains=search_word) | Q(column__name__icontains=search_word)
            article_list = Article.objects.filter(conditon).all()
            # return HttpResponse('OK')
            return render(request,'column_article.html', {'article_list':article_list})
        else:
            return render(request,'column_article.html', {'msg':'未能搜索结果！'})
    if request.method == 'GET':
        return redirect(reverse('fire:index'))


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


def article(request, article_id):
    # 可以直接通过输入url来访问当页面不存在时，我们就要进行相关处理
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


def register(request):
    error1 = '用户名已存在！'
    valid = "用户名可用！"

    if request.method == 'GET':
        form = RegisterForm()
        return render(request,'register.html', {'form':form})
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        # 一种是用户ajax请求，一个时用户提交的请求
        if request.POST.get('raw_username','erjgiqfv240hqp5668ej23foi') != 'erjgiqfv240hqp5668ej23foi':
            try:
                print request.POST.get('raw_username', '')
                user = NewUser.objects.get(username=request.POST.get('raw_username', ''))
            except ObjectDoesNotExist:
                return render(request, 'register.html', {'form':form, 'msg':valid})
        else:
            if form.is_valid():
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                if password1 != password2:
                    return render(request,'register.html', {'form':form, 'msg':'两次密码输入不一致'})
                else:
                    password = make_password(password1)
                    user = NewUser(username=username, email=email, password=password)
                    user.save()
                    return redirect('/fire/login')
            else:
                return render(request, 'register.html',{'form':form})


# 获取分类文章
def get_column(request, column_id):
    column = get_object_or_404(Column, id=column_id)
    article_list = column.article_set.all()
    print  article_list
    return render(request, 'column_article.html', {'article_list':article_list})






