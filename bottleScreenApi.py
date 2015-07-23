# -*- coding:  utf-8 -*-
#!/usr/bin/python
# filename: 
# codedtime: 
from bottle import route, run, request
import ipProxy
import datetime
import os
import subprocess
import sys

def check_login(username, token):
    if username == 'novaqa' and token == '123456':
        return True
    else:
        return False



@route('/login')
def login():
    if request.GET.get('do_submit','').strip(): #点击登录按钮
        # 第一种方式(latin1编码)
        ## username = request.GET.get('username','').strip()  # 用户名
        ## password = request.GET.get('password','').strip()  # 密码

        #第二种方式(获取username\password)(latin1编码)
        getValue = request.query_string
        ## username = request.query['username'] # An utf8 string provisionally decoded as ISO-8859-1 by the server
        ## password = request.query['password'] # 注：ISO-8859-1(即aka latin1编码)
        #第三种方式(获取UTF-8编码)
        username = request.query.username      # The same string correctly re-encoded as utf8 by bottle
        password = request.query.password      # The same string correctly re-encoded as utf8 by bottle
        
        print('getValue=  '+getValue,
              '\r\nusername=  '+username,
              '\r\npassword=  '+password) # test
        
        if check_login(username, password):
            return "<p> Your login information was correct.</p>"
        else:
            return "<p>Login failed. </p>"
    else:
        return ''' <form action="/login" method="get">
                     Username: <input name="username" type="text" />
                     Password: <input name="password" type="password" />
                     <input value="Login" name="do_submit" type="submit">
                   </form>
                '''

@route('/screenshot')
def screenshot():
    username = request.query.username
    token = request.query.token
    if not check_login(username, token):
        return "login failed"

    url = request.query.url
    if url == '':
        return "UrlEmptyError!"
    province = request.query.province
    
    city = request.query.city

    useragent = request.query.useragent
    if useragent == '':
        return "UseragentEmptyError"

    if province == '':
        print("kong")
    region = ''
    if not province == '':
        region = province
    else:
        region = city

    ip = ipProxy.getIpFromRegion(region.encode('utf8'))
    print(ip)
    print(url + " " + ip + " " + region + " " + useragent)
    if ip == "IpNotFonud":
        return "IpNotFonud"

    try:

        # 设置本地的IP
        ipProxy.setProxy(ip)
        

        TIME_FORMAT = '%Y%m%d_%H%M%S'
        currentTime = datetime.datetime.now().strftime(TIME_FORMAT)
        print(currentTime)

        outPutImg = "./snapshot/" + url.replace(".", "").replace("http://www","").replace("/","").replace(":","") +\
                 "_" + region + "_" + useragent + "_" + currentTime + ".png"
        print(outPutImg)

        screenshotScript = "phantomjs screenshot.js " + url + " " + outPutImg + " " + useragent;
        print(screenshotScript)

        # subprocess.call(["phantomjs", "screenshot.js", url, outPutImg.encode(sys.getfilesystemencoding()), useragent],shell=True)
        
        # screenResult = os.popen(screenshotScript.encode(sys.getfilesystemencoding()))
        # 解决了中文乱码问题, 使用subprocess可以使得disableProxy可以有效执行
        screenResult = subprocess.call(screenshotScript.encode(sys.getfilesystemencoding()))
        print(screenResult)

        disableProxyScript = "python ipProxy.py 0"
        os.popen(disableProxyScript)
    except Exception as e:
        print("ERROR: " + str(e.args))
    finally:
        pass



    return username + token

@route('/getCityIp')
def getCityIp():
    username = request.query.username
    token = request.query.token
    if not check_login(username, token):
        return "login failed"

    province = request.query.province
    
    city = request.query.city

    if province == '':
        print("kong")
    region = ''
    if not province == '':
        region = province
    else:
        region = city

    print(region)
    print(type(region))

    ip = ipProxy.getIpFromRegion(region.encode('utf8'))
    print(ip)
    return region + " " + ip


run(host='localhost', port=8083)
