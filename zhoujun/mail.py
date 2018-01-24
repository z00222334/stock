# coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from common import *

def mailresult(ctx, subject):
    if not ctx:
        return
    receiver = 'zjny.my@163.com'
    # subject = 'python email test'
    smtpserver = 'smtp.qq.com'
    sender = 'wudihuoyan@qq.com'
    password = 'Huawei~_123'

    msg = MIMEText(ctx, 'plain', 'utf-8')  # 中文需参数‘utf-8’，单字节字符不需要
    msg['Subject'] = Header(subject, 'utf-8')

    smtp = smtplib.SMTP_SSL(smtpserver, 465)
    smtp.login(sender, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()


def write_result_and_mail(codelist, result_file, subjectname):
    """
    通过代码列表写入信息，主要包含代码、名字、pe、市值等，发送邮件
    :param codelist:
    :return:
    """
    with open(result_file, 'w') as f:
        f.writelines("name,code,pe\n")
        for icode in codelist:
            stockname = get_stockname_from_code(int(icode))
            pe = get_pe_from_code(int(icode))
            linectx = "%s,%s,%s\n" % (icode, stockname, pe)
            f.writelines(linectx)
    with open(result_file, 'r') as f:
        allinfo = f.readlines()
        print('\n'.join(allinfo))
        mailresult(''.join(allinfo), subject=subjectname)
