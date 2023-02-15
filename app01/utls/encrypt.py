# -*- coding: utf-8 -*-
# @Author : John
# @Time : 2023/02/14
# @File : encrypt.py

import hashlib
from DjangoDepartment import settings
# from django.conf import settings


def md5(data_string):
    # salt = 'john'
    # obj = hashlib.md5(salt.encode('utf-8'))
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()


if __name__ == "__main__":
    print(md5('123'))