# 传入文件的后缀，返回该文件的类型
import hashlib

import io
import os


def get_file_type(ext_name):
    photo_file = ['.jpg', '.png', '.gif', '.jpeg']
    movie_file = ['.mp4', '.mkv']
    doc_file = ['.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx', '.pdf', 'txt']
    music_file = ['.mp3']

    ext_name = ext_name.lower()
    if ext_name in photo_file:
        return 2
    elif ext_name in movie_file:
        return 3
    elif ext_name in doc_file:
        return 4
    elif ext_name in music_file:
        return 5

    # 其他文件当做普通文件处理
    return 1


# 根据文件的类型，返回对应的icon
def get_file_icon(file_type):
    if file_type == 0:
        return 'folder_open'

    type_dic = {1: 'insert_drive_file', 2: 'collections', 3: 'movie', 4: 'library_books', 5: 'music_note'}
    return type_dic[file_type]


# 这个是用于显示图片，视频，文档之类的用的
def get_show_type_num(file_type):
    num_dic = {'all': 1, 'photo': 2, 'movie': 3, 'doc': 4, 'music': 5}
    return num_dic[file_type]


# 获取文件的MD5
def get_file_md5(file_path):
    with open(file_path, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        hash_code = md5obj.hexdigest()
        print(hash_code)
        return hash_code


# 获取文件的MD5
def get_md5(path):
    m = hashlib.md5()
    file = io.FileIO(path, 'r')
    block = file.read(1024)
    while block != b'':
        m.update(block)
        block = file.read(1024)
    file.close()

    md5value = m.hexdigest()
    # print(md5value + "  " + path)
    return md5value


# 字节bytes转化kb\m\g
def format_size(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"

    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%.2fG" % (G)
        else:
            return "%.2fM" % (M)
    else:
        return "%.2fkb" % (kb)


# 获取文件大小
def get_file_size(path):
    try:
        size = os.path.getsize(path)
        return format_size(size)
    except Exception as err:
        print(err)



