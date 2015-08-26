# baidu_saveScreenshot
自动化异地跨平台网页截图工具的开发

# 安装方式
##1. 准备
假设这是一台新申请的windows机器，只安装了公司必要的软件
首先，新建文件夹：“D:\baidu\saveScreenshot\”
下载安装git
在此文件夹下将代码从git上下载到本地，得到 baidu_saveScreenshot\
##2. 安装环境
####5. 部署到windows/Linux主机上

目前部署到我的windows主机上，后又部署到了一个台式机上，现在将部署方法总结一下，因为以后还要继续部署：

1. 安装Python27，添加"C:\Python27" 与 "C:\Python27\Scripts" 到path系统变量
2. 安装Python的pip，为以后添加各种程序方便而使用，下载pip安装程序并解压,因为安装到了
    2.1 在以下地址下载最新的PIP安装文件：http://pypi.python.org/pypi/pip#downloads
    2.2 解压到C盘根目录
    2.3 进入这个目录，然后输入 python setup.py install，运行即可
3. 安装phantomjs：
	在[phantomjs官网](http://phantomjs.org/)下载，然后解压，将 phantomjs.exe 直接加入 "C:\Python27\Scripts" 目录即可
4. 安装bottle,tornado,web.py
都是最新版本,因为那边需求一直在变(需要有时候单线程，有时候多线程，能够设置线程池的大小,个人还不理解其必要性,就差使用Spring了)，所以我这边使用了三个框架实现了server，各有优缺点，其中tornado最有潜力
    pip install bottle ：具有单线程(直接启动)和多线程并发执行(使用waitress(pip安装)作为服务器)的模式，单线程的具有根据不同的城市修改代理IP的功能
    pip install tornado ：使用非阻塞的异步来实现，目前是单线程
    pip install web.py ： 在研读其核心模块[源码](http://diaocow.iteye.com/blog/1922760)，修改了web.py的部分源码之后，具有设定线程池大小的功能, 被修改的源码文件在git上，直接覆盖(C:\Python27\Lib\site-packages\web)即可
    由于是启动的是多线程，故增加了logging功能，对不同的进程有一个进程号(目前是自增，比UUID有顺序性)
5. 设置windows定时，[请看链接教程](http://blog.csdn.net/liqfyiyi/article/details/8812971)
6. 配置nginx代理，使能够查看截图，这个简单，直接git下载最新代码即可

####关于flash/*.swf结尾的文件的截图
由于phantomjs对于flash支持得不够好，所以这里目前优先使用selenium完成凯仁给我的5万个flash截图的任务

1. 安装selenium: pip install -U selenium
2. 安装chromedriver，并且放在chrome.exe通目录下，并设置chrome路径在path中（设置环境变量）

在使用代理进行截图的时候遇到了一个bug，就是chromedriver.exe启动之后quit()抛出异常，解决方案如下：
[stackoverflow](http://stackoverflow.com/questions/22018126/selenium-chromedriver-http-407-on-driver-quit). 即 I fixed this problem by opening Internet Options > Connections > LAN settings > Advanced and inserting 127.0.0.1 into the Exceptions box.
