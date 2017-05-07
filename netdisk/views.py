from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from netdisk.forms import RegisterForm
from netdisk.models import User


def index(request):
    show_type = request.GET.get('show_type', 'all')  # 显示的文件类型
    print(show_type)
    return render(request, 'netdisk/index.html')


def login(request):
    if request.method == 'GET':
        return render(request, 'netdisk/login.html')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = None
        try:
            user = User.objects.get(email=email, password=password)
        except Exception:
            print('邮件或者密码错误')

        if user is None:
            return HttpResponse('邮件或者密码错误')
        # 登陆成功
        request.session['user'] = user
        print("登陆完成")
        return HttpResponseRedirect('/')


def logout(request):
    try:
        del request.session['user']  # 不存在时报错
    except Exception:
        print('没有登陆')
    return HttpResponseRedirect('/')


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
