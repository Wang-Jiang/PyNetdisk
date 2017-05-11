import json


class Message(object):
    code = 100
    msg = ''

    # code 100表示成功，200表示出错
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def to_json(self):
        #  ensure_ascii=False 用于防止将中文编程unicode
        return json.dumps({'code': self.code, 'msg': self.msg}, ensure_ascii=False)
