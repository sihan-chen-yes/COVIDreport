# COVIDreporter

* Built a auto reporter via Python
* Used Charles to grasp the http package, then generated a fake one and sent it to the school server
* Considered the accident, if report failed, an email will be sent by the reporter to my phone

COVID autoreport 本以为最迟2020年疫情打卡就会结束 没想到2022年了还在打卡、还在打卡！

~~手写了个玩具实现自动打卡~~

基本思路就是通过软件抓包，获取服务器地址、post/get方式、参数等request信息，借助第三方包，通过python进行打卡，最后利用`linux`的`crontab`命令进行定时执行

使用前请先更改`username`,`password`为自己的BUAA账号和密码

由于不能保证不出现各种意外情况，所以可能会导致没打上卡却误以为打上了的情况，然后被导员嘿嘿嘿

所以采用邮件进行提醒

需要有邮件服务器（选择QQ企业邮箱）来发送提醒邮件

需要自行填写信息的地方有TODO提示，填完即可用

安装依赖：

```
pip install -r requirements.txt
```

`linux`下执行:

```
crontab -e //进行编辑
//加入以下脚本：
30 17 * * * python3 XXX
//XX例如/home/Python/report/report.py
```

脚本执行后会在`py`文件对应路径下生成`log.txt`详细信息

目前为止亲测可用

本人鼓励手动打卡，以上为个人实验，使用此玩具产生的任何后果与本人无关！
