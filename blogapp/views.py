from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Blog
from django.http import JsonResponse
from faker import Faker
from .form import BlogPost
import requests
from bs4 import BeautifulSoup
import re

def home(request):
    blogs = Blog.objects #쿼리셋
    blog_list = Blog.objects.all().order_by('pub_date').reverse()

    totalCount = len(blog_list)
    paginator = Paginator(blog_list, 3)

    count = {}
    count['todo'] = Blog.objects.filter(state=0).count()
    count['doing'] = Blog.objects.filter(state=1).count()
    count['done'] = Blog.objects.filter(state=2).count()

    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    return render(request, 'home.html', {'blogs':blogs, 'posts':posts, 'count':count})

def detail(request, blog_id):
    details = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'detail.html', {'details':details})

def new(request):
    return render(request, 'new.html')

def create(request):
    blog = Blog()
    blog.title = request.POST['title']
    blog.body = request.POST['body']
    blog.pub_date = timezone.datetime.now()
    blog.save()

    # use Faker
    # myfake = Faker('ko_KR')
    # blog.title = myfake.name()
    # blog.body = myfake.address()
    # blog.pub_date = timezone.datetime.now()
    # blog.save()

    return redirect('/blog/' + str(blog.id))

def blogpost(request):
    if request.method == 'POST':
        form = BlogPost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.pub_date = timezone.now()
            post.save()
            return redirect('home')
    else:
        form = BlogPost()
        return render(request, 'new.html', {'form':form})

def movieChart(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    # 네이버 차트 순위 크롤링
    req = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn')
    html = req.text

    soup = BeautifulSoup(html,'html.parser')
    select_chart = soup.select('#old_content > table > tbody > tr > td.title > div > a')
    chart_50 = ''
    for i, movie in enumerate(select_chart):
        print(movie.string)
        chart_50 = chart_50 + (str(i+1) + '. ' + str(movie.text) + '\n')
        
    # 크롤링 데이터 포스팅
    post = Blog()
    post.title = str(timezone.now())[:20] + ' 기준 네이버 영화차트'
    post.body = chart_50
    post.pub_date = timezone.now()
    post.save()
    return redirect('home')

def makeTestPosts(request):
    make = request.GET.get('make')
    if (make == None):
        make = 1
    myfake = Faker()
    for i in range(0,int(make)):
        post = Blog()
        post.title = myfake.name()
        post.body = myfake.address()
        post.pub_date = timezone.datetime.now()
        post.save()
    return redirect('home')

def delete(request, blog_id):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    post = get_object_or_404(Blog, pk=blog_id)
    post.delete()
    return redirect('home')

def update(request, blog_id):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    post = get_object_or_404(Blog, pk=blog_id)
    post.state = int(request.POST.get('state'))
    post.save()
    return redirect('home')
    