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

    return 1
