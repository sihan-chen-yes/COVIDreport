import requests
import json
from datetime import date

login_url = "https://app.buaa.edu.cn/uc/wap/login?redirect=https%3A%2F%2Fapp.buaa.edu.cn%2Fsite%2FbuaaStudentNcov%2Findex"
login_check_url = "https://app.buaa.edu.cn/uc/wap/login/check"
info_url = "https://app.buaa.edu.cn/buaaxsncov/wap/default/get-info"
save_url = "https://app.buaa.edu.cn/buaaxsncov/wap/default/save"

username = "XX" #自己的账号
password = "XX" #自己的密码
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

if __name__ == '__main__':
    login()
    info = get_info()
    post_info(info)






