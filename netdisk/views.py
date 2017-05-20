import os
import random
from datetime import datetime
from itertools import chain

from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render
from django.utils.http import urlquote

from netdisk.forms import RegisterForm
from netdisk.message import Message
from netdisk.models import User, File

# 暂时未考虑显示类型
from netdisk.utils import get_file_type, get_file_icon, get_show_type_num


def index(request):
    show_type = request.GET.get('show_type', 'all')  # 显示的文件类型
    parent_id = request.GET.get('parent_id', 0)  # 父文件夹id
    print(show_type)

    user = request.session['user']
    # 检查父文件夹是否存在
    if parent_id != 0:
        try:
            parent_file = File.objects.get(id=parent_id, user_id=user.id)
        except Exception as error:
            # TODO 404情况
            print(error)

    # 查询并排序
    if show_type is 'all' or show_type is '':
        file_list = File.objects.filter(user_id=user.id, parent_id=parent_id).order_by('file_type', 'id')
    else:
        file_list = File.objects.filter(user_id=user.id, file_type=get_show_type_num(show_type)).order_by('id')

    return render(request, 'netdisk/index.html',
                  {'show_type': show_type, 'parent_id': parent_id, 'file_list': file_list})


def create_folder(request):
    user = request.session['user']
    folder_name = request.POST['folder_name']
    parent_id = request.POST.get('parent_id', 0)  # id为0表示是根目录
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
        # 需要判断后缀变化
        file = File.objects.get(id=file_id, user_id=user.id)
        file.name = file_name
        if file.file_type > 0:
            ext_name = os.path.splitext(file.name)[-1]
            file.file_type = get_file_type(ext_name)

        file.save()
        return HttpResponse('success')
    except Exception as error:
        print(error)
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


# 支持多文件上传
def upload_file(request):
    user = request.session['user']
    files = request.FILES.getlist("file")
    parent_id = request.POST['parent_id']
    for f in files:
        # 获取后缀名，没有考虑，上传的文件没有后缀的情况
        ext_name = os.path.splitext(f.name)[-1]

        # 生成时间戳+随机数字，用于重命名文件，防止文件重名
        target_file_name = datetime.now().strftime('%Y%b%d%H%M%S') + str(random.randint(1000, 9999)) + ext_name
        target_file = open('D:/workspace/PyNetdisk/netdisk/upload/' + target_file_name, 'wb+')
        for chunk in f.chunks():
            target_file.write(chunk)
            # 关闭文件
        target_file.close()

        # 需要工根据相应的后缀，给file_type赋值
        file = File.objects.create(parent_id=parent_id, user_id=user.id, file_type=get_file_type(ext_name), name=f.name,
                                   file_path=target_file.name)
    return HttpResponseRedirect('/?parent_id=' + parent_id)


def download_file(request):
    # 检查文件是否是该用户所有
    user = request.session['user']
    file_id = request.GET.get('file_id', 0)
    try:
        file = File.objects.get(id=file_id, user_id=user.id)

        # 使用迭代器完成，参考 https://blog.oldj.net/2011/07/21/django-big-file-response/
        # http://blog.csdn.net/w6299702/article/details/38777165
        def read_file(fn, buf_size=262144):
            f = open(fn, "rb")
            while True:
                c = f.read(buf_size)
                if c:
                    yield c
                else:
                    break
            f.close()

        # 设定文件头，这种设定可以让任意文件都能正确下载，而且已知文本文件不是本地打开
        response = HttpResponse(read_file(file.file_path), content_type='APPLICATION/OCTET-STREAM')
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(urlquote(file.name))  # 设定传输给客户端的文件名称
        response['Content-Length'] = os.path.getsize(file.file_path)  # 传输给客户端的文件大小
        return response
    except Exception as error:
        print(error)
        return HttpResponse('文件不存在')


# 文件预览功能
def preview_file(request):
    user = request.session['user']
    file_id = request.GET.get('file_id', 0)
    try:
        file = File.objects.get(id=file_id, user_id=user.id)

        def read_file(fn, buf_size=262144):
            f = open(fn, "rb")
            while True:
                c = f.read(buf_size)
                if c:
                    yield c
                else:
                    break
            f.close()

        # 设定文件头
        response = HttpResponse(read_file(file.file_path), content_type='image/jpeg')
        # response['content_type']='image/jpeg'
        response['Content-Length'] = os.path.getsize(file.file_path)  # 传输给客户端的文件大小
        return response
    except Exception as error:
        print(error)
        return HttpResponse('文件不存在')


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


def help_page(request):
    return render(request, 'netdisk/help.html')


def user_info(request):
    if request.method == 'GET':
        # 查看信息
        return render(request, 'netdisk/user-info.html', {'user': request.session['user']})
    elif request.method == 'POST':
        # 保存信息
        user = request.session['user']
        user.username = request.POST['username']
        user.save()

        # print(request.session['user'].username)
        # TODO 出了点问题，session的user信息没有变化，这里采用覆盖来处理
        request.session['user'] = user
        return HttpResponse(Message(100, 'success').to_json(), content_type='application/json')


def change_password(request):
    user = request.session['user']
    old_password = request.POST['old_password']
    new_password = request.POST['new_password']
    repeat_password = request.POST['repeat_password']

    if old_password != user.password:
        return HttpResponse(Message(200, u'密码错误').to_json(), content_type='application/json')

    if new_password is None or new_password == '':
        return HttpResponse(Message(200, u'新密码为空').to_json(), content_type='application/json')

    if new_password != repeat_password:
        return HttpResponse(Message(200, u'两次密码不一致').to_json(), content_type='application/json')

    user.password = new_password
    user.save()
    del request.session['user']
    return HttpResponseRedirect('/login')
