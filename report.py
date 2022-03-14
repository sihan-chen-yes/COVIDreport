import requests
import json
from datetime import date
from smtplib import SMTP_SSL
from email.mime.text import MIMEText

login_url = "https://app.buaa.edu.cn/uc/wap/login?redirect=https%3A%2F%2Fapp.buaa.edu.cn%2Fsite%2FbuaaStudentNcov%2Findex"
login_check_url = "https://app.buaa.edu.cn/uc/wap/login/check"
info_url = "https://app.buaa.edu.cn/buaaxsncov/wap/default/get-info"
save_url = "https://app.buaa.edu.cn/buaaxsncov/wap/default/save"

#todo
username = "XXX" #自己的账号
password = "XXX" #自己的密码
sess = requests.Session()
path = './log.txt'

f = open(path,'a')

def login():
    '''登陆'''
    sess.get(login_url)
    data = {'username':username,'password':password}
    f.write("操作日期:"+ str(date.today()) + "\n")
    f.write("开始登陆" + "\n")
    res = sess.post(url=login_check_url, data=data)
    login_info = json.loads(res.content.decode('utf-8'))
    f.write(str(login_info) + "\n")

def get_info():
    '''获取并填写信息'''
    res = sess.get(info_url)
    res_info = json.loads(res.content.decode('utf-8'))
    stu_info = res_info['d']['oldInfo']
    f.write("获取信息成功" + "\n")
    assert type(res_info['d']['date']) == str
    stu_info['date'] = res_info['d']['date'].replace('-','')
    assert type(stu_info) == dict
    stu_info['is_move'] = 0
    stu_info['realname'] = res_info['d']['uinfo']['realname']
    stu_info['number'] = res_info['d']['uinfo']['role']['number']
    stu_info['gwszdd'] = ''
    f.write("填写信息成功" + "\n")
    return stu_info

def post_info(info):
    f.write("开始上报" + "\n")
    res = sess.post(save_url, data=info)
    res_info = json.loads(res.content.decode('utf-8'))
    f.write(str(res_info) + "\n")
    f.write("操作完毕" + "\n\n")
    f.close()
    if res_info['e'] != 0:
        sendMail()

def sendMail():
    #需要邮件服务器 可用QQ企业邮箱 todo
    user = 'XXX'
    password = 'XXX'
    message = 'There\'s something wrong. Please do the COVID-19 report manually.'
    Subject = 'reporter WA'
    # 发送人
    sender = 'reporter'
    # 收件人
    recipient = 'ito'
    # 收件人邮箱地址 todo
    to_addrs = 'XXX'
    msg = MIMEText(message, 'plain', _charset="utf-8")
    # 邮件主题描述
    msg["Subject"] = Subject
    # 发件人
    msg["from"] = sender
    # 收件人
    msg["to"] = recipient
    with SMTP_SSL(host="smtp.exmail.qq.com", port=465) as smtp:
        # 登录发邮件服务器
        smtp.login(user=user, password=password)
        # 邮件配置
        smtp.sendmail(from_addr=user, to_addrs=to_addrs.split(','), msg=msg.as_string())

if __name__ == '__main__':
    login()
    info = get_info()
    post_info(info)