import requests
import json
from datetime import date
from smtplib import SMTP_SSL
from email.mime.text import MIMEText

login_url = "https://app.buaa.edu.cn/uc/wap/login?redirect=https%3A%2F%2Fapp.buaa.edu.cn%2Fsite%2FbuaaStudentNcov%2Findex"
login_check_url = "https://app.buaa.edu.cn/uc/wap/login/check"
info_url = "https://app.buaa.edu.cn/buaaxsncov/wap/default/get-info"
save_url = "https://app.buaa.edu.cn/buaaxsncov/wap/default/save"

class reporter(object):
    def __init__(self,username,password,user_email,password_email,recipient,to_addrs):
        self.sess = requests.Session()
        path = './log.txt'
        self.f = open(path,'a')
        self.info = ''
        self.username = username
        self.password = password
        self.user_email = user_email
        self.password_email = password_email
        self.recipient = recipient
        self.to_addrs = to_addrs

    def login(self):
        '''登陆'''
        self.sess.get(login_url)
        data = {'username': self.username, 'password': self.password}
        self.f.write("操作日期:" + str(date.today()) + "\n")
        self.f.write("开始登陆" + "\n")
        res = self.sess.post(url=login_check_url, data=data)
        login_info = json.loads(res.content.decode('utf-8'))
        self.f.write(str(login_info) + "\n")

    def get_info(self):
        '''获取并填写信息'''
        res = self.sess.get(info_url)
        res_info = json.loads(res.content.decode('utf-8'))
        stu_info = res_info['d']['oldInfo']
        self.f.write("获取信息成功" + "\n")
        assert type(res_info['d']['date']) == str
        stu_info['date'] = res_info['d']['date'].replace('-', '')
        assert type(stu_info) == dict
        stu_info['is_move'] = 0
        stu_info['realname'] = res_info['d']['uinfo']['realname']
        stu_info['number'] = res_info['d']['uinfo']['role']['number']
        stu_info['gwszdd'] = ''
        self.f.write("填写信息成功" + "\n")
        self.info = stu_info

    def post_info(self):
        self.f.write("开始上报" + "\n")
        res = self.sess.post(save_url, data=self.info)
        res_info = json.loads(res.content.decode('utf-8'))
        self.f.write(str(res_info) + "\n")
        self.f.write("操作完毕" + "\n\n")
        self.f.close()
        if res_info['e'] != 0:
            self.sendMail()

    def sendMail(self):
        message = 'There\'s something wrong. Please do the COVID-19 report manually.'
        Subject = 'reporter WA'
        # 发送人
        sender = 'reporter'
        msg = MIMEText(message, 'plain', _charset="utf-8")
        # 邮件主题描述
        msg["Subject"] = Subject
        # 发件人
        msg["from"] = sender
        # 收件人
        msg["to"] = recipient
        with SMTP_SSL(host="smtp.exmail.qq.com", port=465) as smtp:
            # 登录发邮件服务器
            smtp.login(user=self.user_email, password=self.password_email)
            # 邮件配置
            smtp.sendmail(from_addr=self.user_email, to_addrs=to_addrs.split(','), msg=msg.as_string())

    def reporter_on(self):
        self.login()
        self.get_info()
        self.post_info()

if __name__ == '__main__':
    # BUAA统一身份认证账号、密码 todo
    username = "XXX"
    password = "XXX"
    # 需要邮件服务器 可用QQ企业邮箱 企业邮箱账号、密码
    user_email = 'XXX'
    password_email = 'XXX'
    # 收件人名字、邮箱地址
    recipient = 'XXX'
    to_addrs = 'XXX'
    rep = reporter(username, password, user_email, password_email, recipient, to_addrs)
    rep.reporter_on()