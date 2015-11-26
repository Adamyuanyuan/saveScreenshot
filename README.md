# baidu_saveScreenshot
自动化异地跨平台网页截图工具的开发

# 安装方式_百度内部
##1. 使用mstsc远程连接要安装的windows服务器:
	开始--> 运行--> 输入mstsc
	点选项, 分别输入 172.18.12.134 BDSH00000048068\baidu 密码为 Password123
	如果机器刚打开，则需要登录百度内网准入

注：其它机器

	172.18.12.190 BDSY000067408\baidu Password123 北京
	172.18.12.192 BDSY000067374\baidu Password123 四川
	172.18.12.191 adam-PC\adam Caphi2009 性能差,备用
	172.18.12.135 BDSH00000050167\baidu Password123
-----------------2015.11月，断电后IP更改-----------------
	
	控制机： 
	172.18.12.189 adam-PC\adam Password123
	截图机器：
	北京：172.18.12.134 BDSH00000048068\baidu Password123
	北京：172.18.12.187 BDSY000067408\baidu Password123
	四川：172.18.12.133 BDSH00000050167\baidu Password123
	四川：172.18.12.184 BDSY000067374\baidu Password123


##2. 安装必备环境
所有必备的软件从[http://cq01-testing-ecom6507.cq01.baidu.com:8485/screenShotFiles2.zip](http://cq01-testing-ecom6507.cq01.baidu.com:8485/screenShotFiles2.zip)下载，直接IE浏览器打开这个链接即可下载，里面有 Python27, svn_win64, pip(可不装), gitBash, chrome, chromedriver, phantomjs, nginx(我上传的SVN代码中已有，可不装), sublime(可不装),
下载好之后，解压到D盘，然后进行下述步骤

1. 安装Python27，一直点击下一步即可，添加"C:\Python27;C:\Python27\Scripts" 到path系统变量
    安装好后，进入cmd，输入 python --version 验证是否安装好
2. (这个可以不安装，因为Python27自带pip)安装Python的pip，为以后添加各种程序方便而使用，下载pip安装程序并解压
    2.1 解压pip到C盘根目录
    2.2 进入这个目录，然后输入 python setup.py install，运行即可
3. 安装phantomjs：
	在phantomjs-2.0.0-windows.rar/bin/phantomjs.exe中，将 phantomjs.exe 直接复制到 "C:\Python27\Scripts" 目录即可
	安装好后，进入cmd，输入 phantomjs --version 验证是否安装好
4. 安装selenium: pip install -U selenium
4. 安装svn_win64(需要勾选命令行模式), gitBash(建议安装), sublime(建议安装):一直点击下一步即可

5. 安装chrome, 点击下一步即可，然后将chromedriver 放在chrome.exe所在目录下，并设置chrome路径(一般是C:\Program Files (x86)\Google\Chrome\Application)在path中（设置环境变量）
6. 安装web.py并将我的修改的代码覆盖源代码
   命令行执行 pip install web.py ：修改了web.py的部分源码之后，具有设定线程池大小的功能, 被修改的源码文件在svn上，直接覆盖(源代码在C:\Python27\Lib\site-packages\web)即可
   由于是启动的是多线程，故增加了logging功能，对不同的进程有一个进程号(目前是自增，比UUID有顺序性)
7. 安装python第三方requests包,下载完成后，放到C:\Python27\Lib\requests-master
cmd 切换到 C:\Python27\Lib\requests-master
执行 python setup.py install

##3. 将需要的代码下载下来,然后启动server:
1. SVN下载代码

通过cmd进入D:盘，执行下列命令从SVN中获取需要的代码

	svn export https://svn.baidu.com/app/ecom/nova/trunk/tools/badcase/badcase-server/platform/ideaAnalysisPlatformV2/baidu

2. 设置城市

修改 D:\baidu\saveScreenshot\baidu_saveScreenshot\config.py中的全局变量，来确定不同的城市
比如，我这台172.18.12.134 的机器，如果想作为IP为北京的服务器，则应该如下设置：

	LOCAL_IP_ADDRESS = "http://172.18.12.134/"
    REGION = "beijing"
检测定时抓取代码是否可用，手动执行grapCityIp.py，就会发现有proxList文件被创建，里面放的是可用的IP

3. 启动nginx代理

进入D:\baidu\saveScreenshot\baidu_saveScreenshot\nginx-1.9.2 执行nginx-t 然后执行nginx
然后浏览器输入 http://localhost/nginx-1.9.2/snapshot/test.png，如果显示图片，则说明nginx正常

4. 启动server

进入 D:\baidu\saveScreenshot\baidu_saveScreenshot
执行 
    python webScreenshotService.py numthreads 8083 4 -1 5
如果出现如下信息，则代表启动服务成功

	logs/webpyServiceLogpath not exists and create it
	----test,numthreads:4
	----test,maxthreads:-1
	----test,request_queue_size:5
	http://0.0.0.0:8083/

试一下：

    http://172.18.12.134/WebScreenshot?isFlash=true&url=http://ubmcmm.baidustatic.com/media/v1/0f0005TkYRYWPBHoEyanj0.swf%3Furl_type=1%26snapsho=%26&useragent=pcChrome&username=novaqa&token=123456

    http://172.18.12.134/WebScreenshot?isFlash=false&url=http://www.baidu.com&useragent=pcChrome&username=novaqa&token=123456


##4. 设置windows定时计划任务
可以参考这个教程：[请看链接教程](http://blog.csdn.net/liqfyiyi/article/details/8812971)
###1.python_grapIpProxy
1. 菜单-->输入 计划 --> 打开 "任务计划程序"-->操作-->导入任务--> D:\baidu\saveScreenshot\baidu_saveScreenshot\taskScanner\python_grapIpProxy.xml
2. 这时会有个任务导入，在 "常规"面板 修改"更改用户或组" 然后在"输入要选择的对象名称"输入"baidu"-->检查名称-->确定
3. 选择 "不管用户是否登陆都要运行+不存储密码"，点击确定即可

###2.python_grapIpProxy
1. 菜单-->输入 计划 --> 打开 "任务计划程序"-->操作-->导入任务--> D:\baidu\saveScreenshot\baidu_saveScreenshot\taskScanner\python_checkAndSetCityIp.xml
2. 这时会有个任务导入，在 "常规"面板 修改"更改用户或组" 然后在"输入要选择的对象名称"输入"baidu"-->检查名称-->确定
3. 选择 "不管用户是否登陆都要运行+不存储密码"，点击确定即可

现在这些计划任务还没有被启动，在任务面板中将其设置为启用就OK

好，恭喜你，至此，server就搭建起来了，因为是在windows上搭建的，并且需要安装一些软件，所以比较麻烦