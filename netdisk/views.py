from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from netdisk.forms import RegisterForm
from netdisk.models import User, File


# 暂时未考虑显示类型
def index(request):
    show_type = request.GET.get('show_type', 'all')  # 显示的文件类型
    parent_id = request.GET.get('parent_id', 0)  # 父文件夹id
    print(show_type)

    user = request.session['user']
    file_list = File.objects.get(user_id=user.id, parent_id=parent_id)
    print(file_list)
    return render(request, 'netdisk/index.html', {'show_type': show_type, 'parent_id': parent_id, 'file_list': file_list})


def create_folder(request):
    user = request.session['user']
    folder_name = request.POST['folder_name']
    parent_id = request.POST.get('paren_id', 0)  # id为0表示是根目录
    folder = File.objects.create(parent_id=parent_id, user_id=user.id, file_type=0, name=folder_name,
                                 create_time=datetime.now())
    return HttpResponseRedirect('/')


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
