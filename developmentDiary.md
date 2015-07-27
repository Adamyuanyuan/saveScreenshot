##自动跨地域截图工具

随着第一个项目，创意挖掘分析网站第二版本的基本告一段落，我又迎来了第二个大任务，是一个非常有意思的任务，做一个自动跨地域截图工具，这个工具之前没有人做过，我先整理一下思路：
通过前期考察，决定使用语言: nodeJS + python  使用工具: phantomjs + urlib

1. 制作一个简单的网页，实现不同地域不同浏览器型号显示不同的界面
这个网站可以让我理解他们跨地域跨平台显示不同界面的网页的原理，并且作为之后工具的测试
已写好，直接输出地域和平台信息
2. 制作自动跨地域截图工具，为测试人员提供一个http的GET的API接口，流程如下
输入：URL+地域+useragent
2.1 自动打开Chrome
2.2 设置发给浏览器的参数 useragent 某个地域的IP(这里需要实现并维护一个自动每个地域与代理IP的对应表，定时从一个网页上抓取不同地域的IP信息工具)
2.3 自动向网页输入URL，并且自动访问
2.4 将访问的网页自动截图，并保存到本地，并返回截图url，关闭chrome

####1. 通过修改不同的useragent来访问网页并截图

这个是用phantomjs来实现，代码脚本在: screenshot.js,调用方式为:	
	phantomjs screenshot.js url outPutImg userAgentType
 url : 网址
 outPutImg : 保存图片名称(与路径)
 userAgentType : 目前支持: [pc_chrome|pc_firefox|pc_ie8|android|iphone]

####2. 脚本自动化设置代理IP
目前已经解决了自动化设置代理中设置不能自动刷新的问题，使用方法如下：
设置为北京的代理：
	python ipProxy.py 219.142.192.196:1604

####3. 抓取不同地区的代理IP信息
通过Python网页爬虫抓取不同地区的代理IP信息并保存成属性文件的形式，用来设置浏览器的代理IP
1.  使用5个线程抓取xici网站的5个国内代理IP页面，然后通过网站上的连接时间进行排序,并保存至proxy_list_before.%Y%m%d_%H；
2. 使用20个线程通过百度进行验证其有效性，将有效的代理IP按照实际测出的连接时间排序，并保存至proxy_list_after.%Y%m%d_%H

使用方法如下：
	python grapCityIp
将会保存"proxy_list_before"与"proxy_list_after"两个省份与城市的代理IP列表，其中proxy_list_after是经过验证的
这个列表每一个小时更新一次

使用windows/linux自动计划任务，来每隔一小时执行一次上述命令

####4. 使用Python—bottle编写GET API，将所有内容综合起来，并返回Json数据
api_1: screenshot 通过省份得到固定网页的截图 输入：url=http://www.baidu.com&province=beijing&city=北京&useragent=pcChrome&username=novaqa&token=123456

	http://http://172.18.12.191/v1/screenshot?url=http://www.baidu.com&province=beijing&city=北京&useragent=pcChrome&username=novaqa&token=123456

return Json:

	{
	  "screenshot_url":"http://http://172.18.12.191//screenshot/wwwbaiducom_beijing_pcChrome_201507221032.png"
	}

api_2: getCityIp 通过省份得到对应的代理IP

	http://http://172.18.12.191/v1/getCityIp?province=beijing&city=北京&username=novaqa&token=123456

return Json:

	{
		"region" : "北京"
	    "proxyIp":"220.181.143.14:9999"
	}

####5. 部署到windows/Linux主机上

目前部署到我的windows主机上，使用了nginx代理