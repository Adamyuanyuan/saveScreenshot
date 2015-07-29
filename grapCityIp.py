# -*- coding:  utf-8 -*-
#!/usr/bin/python
"""
实现从网站抓取代理网站的IP并且验证其可靠性的工具，最后将结果保存到文件中.

Authors: wangxiaogang02(wangxiaogang02@baidu.com)
Date:    2015/07/27 17:23:06
"""

import urllib2
import re
import threading
import time
import datetime
import sys

rawProxyList = []
checkedProxyList = []

#抓取代理网站
targets=[]
target = r"http://www.xici.net.co/nt/"
targets.append(target)
print targets

#正则
p = re.compile(r'''<tr class=".+?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>.+?(\d{2,4})</td>.+?<td>(.{4,5})</td>''',re.DOTALL)
P_ALL = re.compile(r'''<tr class=".+?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>.+?(\d{2,5})</td>.+?<td>.+?<a href=\"/.+?/(.{2,15})\">(.+?)</a>.+?title=\"(.{3,10})\" class=\"bar''',re.DOTALL)
p_hebei = re.compile(r'''<tr class=".+?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>.+?(\d{2,5})</td>.+?hebei\">(.+?)</a>.+?<td>(.{4,5})</td>''',re.DOTALL)
p_beijing = re.compile(r'''<tr class=".+?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>.+?(\d{2,5})</td>.+?beijing\">(.+?)</a>.+?<td>(.{4,5})</td>''',re.DOTALL)
p_anhui = re.compile(r'''<tr class=".+?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>.+?(\d{2,5})</td>.+?anhui\">(.+?)</a>.+?<td>(.{4,5})</td>''',re.DOTALL)
p_shanghai = re.compile(r'''<tr class=".+?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>.+?(\d{2,5})</td>.+?shanghai">(.+?)</a>.+?<td>(.{4,5})</td>''',re.DOTALL)

#获取代理的类
class ProxyGet(threading.Thread):
    def __init__(self,target,p):
        threading.Thread.__init__(self)
        self.target = target
        self.p = p

    def getProxy(self):
        print "目标网站：" + self.target
        req = urllib2.urlopen(self.target)
        result = req.read()
        matchs = self.p.findall(result)
        for row in matchs:
            ip = row[0]
            port = row[1]
            # 英文省份名称
            province_en = row[2]
            # 中文所在城市名称
            city_cn = row[3]
            speed = row[4]
            proxy = [ip,port,province_en,city_cn,speed]
            # print(proxy)
            rawProxyList.append(proxy)

    def run(self):
        self.getProxy()

#检验代理类
class ProxyCheck(threading.Thread):
    def __init__(self,proxyList):
        threading.Thread.__init__(self)
        self.proxyList = proxyList
        self.timeout = 5
        self.testUrl = "http://www.baidu.com/"
        self.testStr = "030173"

    def checkProxy(self):
        cookies = urllib2.HTTPCookieProcessor()
        for proxy in self.proxyList:
            proxyHandler = urllib2.ProxyHandler({"http" : r'http://%s:%s' %(proxy[0],proxy[1])})
            opener=urllib2.build_opener(cookies,proxyHandler)
            opener.addheaders =[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36')]
            t1 = time.time()
            try:
                req = opener.open(self.testUrl,timeout=self.timeout)
                result=req.read()
                timeused = time.time()-t1
                pos = result.find(self.testStr)

                if pos > 1:
                    checkedProxyList.append((proxy[0],proxy[1],proxy[2],proxy[3],timeused))
                    print "ok ip: %s %s %s %s %s" %(proxy[0],proxy[1],proxy[2],proxy[3],timeused)
                else:
                    continue
            except Exception,e:
                continue

    def run(self):
        self.checkProxy()


def main():
    getThreads=[]
    checkThreads=[]

    #对每个目标网站开启一个线程负责抓取代理
    for i in range(len(targets)):
        p_city = P_ALL
        t_city = ProxyGet(targets[i], p_city)
        getThreads.append(t_city)

    for i in range(len(getThreads)):
        getThreads[i].start()

    for i in range(len(getThreads)):
        getThreads[i].join()

    print '.' * 10 + "总共抓取了%s个代理" % len(rawProxyList) + '.' * 10

    TIME_FORMAT = '%Y%m%d_%H'
    # today = datetime.date.today()
    # 此处windows处路径为\,若转为Linux下服务，可能需要修改
    fileBeforePath = "proxyList/proxyListRaw." + time.strftime(TIME_FORMAT)
    fileAfterPath = "proxyList/proxyListAfter." + time.strftime(TIME_FORMAT)
    #持久化验证前的数据
    fileBefore = open(fileBeforePath,'w+')
    for proxy in sorted(rawProxyList, cmp=lambda x,y:cmp(x[4],y[4])):
        print "write raw proxy is: %s:%s\t%s\t%s\t%s" %(proxy[0],proxy[1],proxy[2],proxy[3],proxy[4])
        fileBefore.write("%s:%s\t%s\t%s\t%s\n"%(proxy[0],proxy[1],proxy[2],proxy[3],proxy[4]))
    fileBefore.close()


    #开启20个线程负责校验，将抓取到的代理分成20份，每个线程校验一份
    for i in range(20):
        t = ProxyCheck(rawProxyList[((len(rawProxyList)+19)/20) * i:((len(rawProxyList)+19)/20) * (i+1)])
        checkThreads.append(t)

    for i in range(len(checkThreads)):
        checkThreads[i].start()

    for i in range(len(checkThreads)):
        checkThreads[i].join()

    print '.' * 10 + "总共有%s个代理通过校验" %len(checkedProxyList) + '.' * 10

    #持久化验证后的数据
    fileAfter = open(fileAfterPath,'w+')
    for proxy in sorted(checkedProxyList,cmp=lambda x,y:cmp(x[4],y[4])):
        print "checked proxy is: %s:%s\t%s\t%s\t%s" %(proxy[0],proxy[1],proxy[2],proxy[3],proxy[4])
        fileAfter.write("%s:%s\t%s\t%s\t%s\n"%(proxy[0],proxy[1],proxy[2],proxy[3],proxy[4]))
    fileAfter.close()

if __name__ == "__main__":
        main()
