# 传入文件的后缀，返回该文件的类型
def get_file_type(ext_name):
    photo_file = ['.jpg', '.png', '.gif', '.jpeg']
    movie_file = ['.mp4', '.mkv']
    doc_file = ['.doc', '.ppt', '.xls', '.pdf']
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