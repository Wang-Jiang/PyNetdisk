from django.http import HttpResponse
from django.shortcuts import render

from netdisk.forms import RegisterForm
from netdisk.models import User


def index(request):
    return HttpResponse('测试')


def login(request):
    if request.method == 'GET':
        return render(request, 'netdisk/login.html')
    elif request.method == 'POST':
        pass


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # 查询一下这个邮箱有没被注册过
            try:
                User.objects.get(email=email)
                return HttpResponse('邮箱已经被注册')
            except Exception:
                print('没有注册')

            User.objects.create(username=username, email=email, password=password)
            return HttpResponse(email + '注册成功')



