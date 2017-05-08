from datetime import datetime
from itertools import chain

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
    # 检查父文件夹是否存在
    try:
        parent_file = File.objects.get(id=parent_id, user_id=user.id)
    except Exception as error:
        # TODO 404情况
        print(error)

    file_list = File.objects.filter(user_id=user.id, parent_id=parent_id)

    print(file_list)
    return render(request, 'netdisk/index.html',
                  {'show_type': show_type, 'parent_id': parent_id, 'file_list': file_list})


def create_folder(request):
    user = request.session['user']
    folder_name = request.POST['folder_name']
    parent_id = request.POST.get('paren_id', 0)  # id为0表示是根目录
    folder = File.objects.create(parent_id=parent_id,
                                 user_id=user.id,
                                 file_type=0,
                                 name=folder_name,
                                 create_time=datetime.now())
    return HttpResponseRedirect('/?parent_id=' + parent_id)


def edit_name(request):
    # 判断文件所有情况
    file_id = request.POST['id']
    file_name = request.POST['name']
    user = request.session['user']
    try:
        file = File.objects.get(id=file_id, user_id=user.id)
        file.name = file_name
        file.save()
        return HttpResponse('success')
    except Exception:
        return HttpResponse('error')


def delete_file(request):
    file_id = request.POST['id']
    user = request.session['user']
    try:
        file = File.objects.get(id=file_id, user_id=user.id)
        file_list = File.objects.filter(parent_id=file.id)
        # 需要删除改目录下所有文件
        for item in file_list:
            # 将item的下一级子目录加入
            chain(file_list, File.objects.filter(parent_id=item.id))

        print(file_list)

        file.delete()  # 删除文件记录
        # 删除file_list的所有数据，即将file的子目录全部删除
        for item in file_list:
            item.delete()

        return HttpResponse('success')
    except Exception as error:
        print('error:', error)
        return HttpResponse('error')


def upload_file(request):

    pass


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
