# coding: utf-8

import platform

def get_sep():
    """
    获取系统类型然后根据系统类型获得路径分隔符
    """
    if platform.system() == "Darwin":
        sep = "/"
    else:
        sep = "\\"
    # print "system sep is %s" % sep
    return sep
