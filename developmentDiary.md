##自动跨地域截图工具
###前期调研
随着第一个项目，创意挖掘分析网站第二版本的基本告一段落，我又迎来了第二个大任务，是一个非常有意思的任务，做一个自动跨地域截图工具，这个工具之前没有人做过，我先整理一下思路：
通过前期考察，决定使用语言: nodeJS + python  使用工具: phantomjs + urlib

1. 制作一个简单的网页，实现不同地域不同浏览器型号显示不同的界面
这个网站可以让我理解他们跨地域跨平台显示不同界面的网页的原理，并且作为之后工具的测试
已写好，直接输出地域和平台信息
2. 制作自动跨地域截图工具，为测试人员提供一个http的GET的API接口，流程如下
输入：URL+地域+useragent
- 2.1 自动打开Chrome（模拟）
- 2.2 设置发给浏览器的参数 useragent 某个地域的IP(这里需要实现并维护一个自动每个地域与代理IP的对应表，定时从一个网页上抓取不同地域的IP信息工具)
- 2.3 自动向网页输入URL，并且自动访问
- 2.4 将访问的网页自动截图，并保存到本地，并返回截图url，关闭chrome

###中期总结
####项目背景：
有些广告很贼，对不同地域的用户和不同浏览器的用户显示不同的结果来躲避排查，而我的工具要做的就是模拟不同地域和不同浏览器的用户，访问那个网站，并且将网页信息截图并排查，净化网盟广告，降低投诉，推动产品效果提升
####项目目标：
开发出一个比较可靠可用的分地域/useragent截图工具API，供大家使用

#####1.	代理IP的定时抓取保存
重点：对网页上的IP地址进行匹配，并使用www.baidu.com其可用性验证
难点：

1.	由于西祠网站上有的IP有图片，有的IP是没有图片的，所以写出一个通用的正则表达式来判断它们的比较困难的（已解决）
2.	网页中抓取的IP不稳定的问题（后期寻找其它代理IP的途径）
效果：完成了从西祠网站上多线程下载各个城市代理IP并自动测试其可用性的功能，每小时更新一次最新的代理IP并保存到文件

#####2.	修改代理IP来模拟不同地域的机器
重点：通过修改windows注册列表来更改本地的代理IP
难点：修改注册表后，系统代理设置并不能实时更新（借助ctypes解决）
效果：实现了自动化修改本地的代理IP
#####3.	通过设置useragent和进行网页截图
重点：如何模拟或者实现通过浏览器访问网页并截图
难点：目前通用的截图方案有通过Python直接模拟打开浏览器并操作浏览器截图和通过phantomjs 模拟后天webkit内核进行截图，（后者的方案具有更高的可移植性和跟强的性能）
效果：用node.js实现了通过不同useragent访问指定网页并截图，完善函数功能，目前支持：[pc_chrome|pc_firefox|pc_ie8|android|iphone]等浏览器的访问，并制定图片保存路径，并在截图的时候对页面上所有链接添加标注
#####4.	截图工具API的编写
重点：截图工具API要具有不太差的性能和良好的稳定性
难点：

1.	需求1：我需要用Python自己实现一个简单的server并部署，以便以后能够容易修改。
方案1：我不太倾向于自己写复杂的轮子，效率低也没有太必要，所以用了一个最简单的bottle框架对这个需求进行了折中，目前已经用三个框架将其实现
2.	需求2：由于这个API需要修改注册列表，所以同一时间只能对同一个地域的VPN进行截图，所以须得保证单位时间只能处理一个请求，而其它请求需要完成一个排队的机制，我需要实现一个简单可依赖的方法解决这个问题，而不要自己去开发线程阻塞。
方案2：正在调研中
3.	截图工具的部署，因为目前要部署在windows下，这个待前两个问题解决了再说。
应该是可以部署在Linux下的，只不过可能会遇到：
3.1	Linux下百度内网安装phantomjs工具的问题
3.2	Linux下截图显示不了汉字的问题
3.3	一些中文字库不全的问题
3.4	测试机不够用的问题，因为要动态修改本地IP，这个可以考虑使用多个虚拟机，然后使用nginx转发多个不同的虚拟机来解决
效果：目前截图工具可以在windows局域网内进行使用
#####5后面计划：schedule/ todo list
1.	完成截图工具API的编写
2.	部署到一台专用机器上

###过程记录
####1. 通过修改不同的useragent来访问网页并截图

这个是用phantomjs来实现，代码脚本在: screenshot.js,调用方式为:	
	phantomjs screenshot.js url outPutImg userAgentType
 url : 网址
 outPutImg : 保存图片名称(与路径)
 userAgentType : 目前支持: [pc_chrome|pc_firefox|pc_ie8|android|iphone]
遇到了大问题：这个工具不支持flash，比如如下url截图就会有问题：
http://localhost:8083/v1/screenshot?url=http://www.dhs.state.il.us/accessibility/tests/flash/video.html&city=%E4%B8%8A%E6%B5%B7&useragent=pcChrome&username=novaqa&token=123456

####2. 脚本自动化设置代理IP
目前已经解决了自动化设置代理中设置不能自动刷新的问题，使用方法如下：
设置为北京的代理：
	python ipProxy.py 219.142.192.196:1604

####3. 抓取代理IP信息
######抓取不同地区的代理IP信息
通过Python网页爬虫抓取不同地区的代理IP信息并保存成属性文件的形式，用来设置浏览器的代理IP

1. 使用5个线程抓取xici网站的5个国内代理IP页面，然后通过网站上的连接时间进行排序,并保存至proxy_list_before.%Y%m%d_%H；
2. 使用20个线程通过百度进行验证其有效性，将有效的代理IP按照实际测出的连接时间排序，并保存至proxy_list_after.%Y%m%d_%H

使用方法如下：
	python grapCityIp
将会保存"proxy_list_before"与"proxy_list_after"两个省份与城市的代理IP列表，其中proxy_list_after是经过验证的
这个列表每一个小时更新一次

使用windows/linux自动计划任务，来每隔一小时执行一次上述命令

######抓取同一地区的代理IP信息
由于需要并行操作，所以我这边需要完成抓取同一地区的代理IP信息，并验证其有效性，将其保存为一个列表

####4. 使用Python—bottle编写GET API，将所有内容综合起来，并返回Json数据
api_1: screenshot 通过省份得到固定网页的截图 输入：url=http://www.baidu.com&province=beijing&city=北京&useragent=pcChrome&username=novaqa&token=123456

	http://172.18.12.191/v1/screenshot?url=http://www.baidu.com&province=beijing&city=北京&useragent=pcChrome&username=novaqa&token=123456

return Json:

	{
	  "screenshot_url":"http://172.18.12.191/screenshot/wwwbaiducom_beijing_pcChrome_201507221032.png"
	}

api_2: getCityIp 通过省份得到对应的代理IP

	http://172.18.12.191/v1/getCityIp?province=beijing&city=北京&username=novaqa&token=123456

return Json:

	{
		"region" : "北京"
	    "proxyIp":"220.181.143.14:9999"
	}

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

3. 在fileSrc_temp_file_%d 文件的第 10, 100, 1000行分别插入违规flash进行对比
	000000010	1	flash_000000010_1.png	http://ubmcmm.baidustatic.com/media/v1/0f0005PfIe3eITOWMDdeDs.swf
	0000000100	1	flash_0000000100_1.png	http://ubmcmm.baidustatic.com/media/v1/0f0005PfIe3eITOWMDdeDs.swf
	。。。
	
4. 执行 python screenShotFlashFromFile2.py fileSrc_temp_file_1 即可

#### 使用Python—web.py编写GET API，将所有内容综合起来，并返回Json数据
api_1: screenshot 通过省份得到固定网页的截图 输入：isFlash=true&url=http://ubmcmm.baidustatic.com/media/v1/0f0005TkYRYWPBHoEyanj0.swf%3Furl_type=1%26snapsho=%26&useragent=pcChrome&username=novaqa&token=123456

参数详解:

- isFlase=[true|false] : 是否截取静态flash，默认为false,只有参数为true的时候才有效
- url=http://ubmcmm.baidustatic.com/media/v1/0f0005TkYRYWPBHoEyanj0.swf%3Furl_type=1%26snapsho=%26 : 要截图的网页或者静态文件的url，如果url中有特殊字符，则需要转义，我会随后写个转义的小脚本给大家使用
- useragent=pcChrome，useragent设置，只对网页截图(isFlash=false)有效，目前支持: [pc_chrome|pc_firefox|pc_ie8|android|iphone]
- username=novaqa&token=123456 固定的用户名和密码，为与网盟其它API一致
- dirName=testImageDir : 图片保存文件夹参数，可选，用于自动化截图后的打包,默认 flashSnapshot_地区拼音_日期
- imageName=testImageName ： 图片保存名称参数，可选，用于保存的图片名，默认 url(取出特殊字符)_地区拼音_useragent_时间戳.png


	http://172.18.12.191:8083/WebScreenshot?isFlash=true&url=http://ubmcmm.baidustatic.com/media/v1/0f0005TkYRYWPBHoEyanj0.swf%3Furl_type=1%26snapsho=%26&useragent=pcChrome&username=novaqa&token=123456&dirName=testImageDir&imageName=testImageName

return Json:

	{
	  'screenshotUrl':'http://172.18.12.191/flashSnapshot/flashSnapshot_all_20150806/ubmcmmbaidustaticcommediav10f0005TkYRYWPBHoEyanj0swf_all_pcChrome_20150806_145645.png'
	}
