#coding:utf-8
#author zhoujun


"""
提供日志方法
"""
import logging

logging.basicConfig(filename="stock.log",
                    format="%(asctime)s %(message)s",
                    level=logging.DEBUG)
