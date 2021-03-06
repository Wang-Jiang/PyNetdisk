from datetime import datetime

from django.db import models


class User(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    username = models.CharField(max_length=32)
    avatar = models.CharField(max_length=128, default='/static/themes/images/user-icon.png')
    email = models.EmailField(max_length=32, unique=True)
    password = models.CharField(max_length=32)


class File(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    parent_id = models.IntegerField(default=0)  # 0表示是根目录
    user_id = models.IntegerField()
    file_type = models.IntegerField(default=0)  # 0表示是文件夹，1表示普通文件，2表示图片，3表示视频，4表示文档，5表示音乐
    name = models.CharField(max_length=64)
    create_time = models.DateTimeField(default=datetime.now)
    file_path = models.CharField(max_length=128)  # 当类型是文件的时候，这个字段才有用，它是存放文件的具体位置
    file_md5 = models.CharField(max_length=32, default='')  # 文件的MD5
    file_size = models.CharField(max_length=10, default='0B')  # 文件的大小，已经被格式化
