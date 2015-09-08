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
import os

import config
import ipProxy

rawProxyDir = {}
checkedProxyList = {}

#抓取代理网站1： 西祠代理网站
XC_targets=[]
XC_target = r"http://www.xici.net.co/nt/"
XC_targets.append(XC_target)
print XC_targets

XC_cityCompileMap = {}
#正则
XC_all = re.compile(r'''<tr class=".+?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>.+?(\d{2,5})</td>.+?<td>.+?<a href=\"/.+?/(.{2,15})\">(.+?)</a>.+?title=\"(.{3,10})\" class=\"bar''', re.DOTALL)
XC_hebei = re.compile(r'''<tr class=".+?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>.+?(\d{2,5})</td>.+?<td>.+?<a href=\"/.+?/(hebei)\">(.+?)</a>.+?title=\"(.{3,10})\" class=\"bar''', re.DOTALL)
# XC_beijing = re.compile(r'''<tr class=".+?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>.+?(\d{2,5})</td>.+?(beijing)\">(.+?)</a>.+?title=\"(.{3,10})\" class=\"bar''',re.DOTALL)
XC_beijing = re.compile(r'''<tr class=".+?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>.+?(\d{2,5})</td>.+?(beijing)\">(.+?)</a>.+?<td>(.{4,5})</td>''', re.DOTALL)
# XC_beijing = re.compile(r'''<tr class=".+?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>.+?(\d{2,5})</td>.+?<td>.+?<a href=\"/.+?/(beijing)\">(.+?)</a>.+?title=\"(.{3,10})\" class=\"bar''', re.DOTALL)
XC_shandong = re.compile(r'''<tr class=".+?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>.+?(\d{2,5})</td>.+?(shandong)\">(.+?)</a>.+?title=\"(.{3,10})\" class=\"bar''', re.DOTALL)
XC_shanghai = re.compile(r'''<tr class=".+?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>.+?(\d{2,5})</td>.+?(shanghai)\">(.+?)</a>.+?title=\"(.{3,10})\" class=\"bar''', re.DOTALL)
XC_jiangxi = re.compile(r'''<tr class=".+?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>.+?(\d{2,5})</td>.+?(jiangxi)\">(.+?)</a>.+?<td>(.{4,5})</td>''', re.DOTALL)
XC_sichuan = re.compile(r'''<tr class=".+?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>.+?(\d{2,5})</td>.+?(sichuan)\">(.+?)</a>.+?<td>(.{4,5})</td>''', re.DOTALL)

XC_cityCompileMap["all"] = XC_all
XC_cityCompileMap["beijing"] = XC_beijing
XC_cityCompileMap["hebei"] = XC_hebei
XC_cityCompileMap["shandong"] = XC_shandong
XC_cityCompileMap["shanghai"] = XC_shanghai
XC_cityCompileMap["jiangxi"] = XC_jiangxi
XC_cityCompileMap["sichuan"] = XC_sichuan

#抓取代理网站2： 好代理网站
HDL_cityUrlMap = {}
HDL_cityUrlMap["all"] = r"http://www.haodailiip.com/guonei/"
HDL_cityUrlMap["beijing"] = r"http://www.haodailiip.com/guonei/110000/"
HDL_cityUrlMap["jiangxi"] = r"http://www.haodailiip.com/guonei/360000/"
HDL_cityUrlMap["sichuan"] = r"http://www.haodailiip.com/guonei/510000/"
HDL_cityUrlMap["hebei"] = r"http://www.haodailiip.com/guonei/130000/"
HDL_cityUrlMap["shandong"] = r"http://www.haodailiip.com/guonei/370000/"

HDL_targets=[]
# 如果是要抓取所有城市的IP，则需要开多个线程抓取多个页面的数据，如果一个IP一个页面的IP够
if config.REGION == "all":
    for i in range(1, 10):
        HDL_target = HDL_cityUrlMap["all"] + str(i)
        HDL_targets.append(HDL_target)
else:
    # 如果代理的数量太多，则会被此网站禁止，目前有一个页面的IP就够用了
    for i in range(1, 2):
        HDL_target = HDL_cityUrlMap[config.REGION] + str(i)
        HDL_targets.append(HDL_target)
print HDL_targets

HDL_cityCompileMap = {}
#正则
HDL_all = re.compile(r'''<td>.+?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).+?</td>.+?(\d{2,5}).+?</td>.+?<td>(.+?) (.+?) .+?</td>.+?</td>.+?(\d.{1,8}ms)</td>''', re.DOTALL)
HDL_beijing = re.compile(r'''<td>.+?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).+?</td>.+?(\d{2,5}).+?</td>.+?<td>(.+?) (.+?) .+?</td>.+?</td>.+?(\d.{1,8}ms)</td>''', re.DOTALL)

# 它们的正则表达式是一样的
HDL_cityCompileMap["all"] = HDL_all
HDL_cityCompileMap["beijing"] = HDL_beijing
HDL_cityCompileMap["jiangxi"] = HDL_beijing
HDL_cityCompileMap["sichuan"] = HDL_beijing
HDL_cityCompileMap["hebei"] = HDL_beijing
HDL_cityCompileMap["shandong"] = HDL_beijing


def getProxyFromFile(region):
    """读取以前保存的城市的IP供可用性检查"""
    try:
        TIME_FORMAT = '%Y%m%d_%H'
        currentHour = datetime.datetime.now()
        lastHour = currentHour - datetime.timedelta(hours = 1)
        last2Hour = currentHour - datetime.timedelta(hours = 2)

        isFileOpened = False

        fileAfterPath = "proxyList/" + region + "/proxyListAfter." \
                + lastHour.strftime(TIME_FORMAT)
        if not os.path.isdir("proxyList/" + region):
            os.makedirs("proxyList/" + region)
        if not os.path.exists(fileAfterPath):
            print("Use before hour proxy list")
            fileAfterPath = "proxyList/" + region + "/proxyListAfter." \
                + last2Hour.strftime(TIME_FORMAT)
        if not os.path.exists(fileAfterPath):
            print("FileAfterPath not exists")
            return

        readFile = open(fileAfterPath, "r")
        isFileOpened = True
        
        for eachLine in readFile:
            lineArray = eachLine.strip('\n').split('\t')
            rawProxyDir[lineArray[0]] = lineArray
            print(lineArray)
        
    except Exception as e:
        print("ERROR: " + str(e.args))
    finally:
        if(isFileOpened):
            readFile.close()


class ProxyGet(threading.Thread):
    """获取代理的类"""
    def __init__(self, target, p):
        threading.Thread.__init__(self)
        self.target = target
        self.p = p

    def getProxy(self):
        """从目标网站得到IP代理"""
        print "目标网站：" + self.target
        req = urllib2.urlopen(self.target)
        result = req.read()
        matchs = self.p.findall(result)
        for row in matchs:
            ip = row[0]
            port = row[1]
            # 英文省份名称
            province_en = row[2]
            # province_en = config.REGION
            # 中文所在城市名称
            city_cn = row[3]
            speed = row[4]
            proxy = [ip + ":" + port, province_en, city_cn, speed]
            print(proxy)
            rawProxyDir[proxy[0]] = proxy

    def run(self):
        self.getProxy()


class ProxyCheck(threading.Thread):
    """检验代理类"""
    def __init__(self, proxyList):
        threading.Thread.__init__(self)
        self.proxyList = proxyList
        self.timeout = 5
        self.testUrl = "http://www.baidu.com/"
        self.testStr = "030173"

    def checkProxy(self):
        """检验代理类方法"""
        cookies = urllib2.HTTPCookieProcessor()
        for proxy in self.proxyList:
            proxyHandler = urllib2.ProxyHandler({"http": r'http://%s' % (proxy[0])})
            opener = urllib2.build_opener(cookies, proxyHandler)
            opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36')]
            t1 = time.time()
            try:
                req = opener.open(self.testUrl, timeout = self.timeout)
                result = req.read()
                timeused = time.time() - t1
                pos = result.find(self.testStr)

                if pos > 1:
                    checkedProxyList[proxy[0]] = [proxy[0], proxy[1], proxy[2], proxy[3], timeused]
                    print "ok:%s %s %s %s %s" % (proxy[0], proxy[1], proxy[2], proxy[3], timeused)
                else:
                    continue
            except Exception as e:
                continue

    def run(self):
        self.checkProxy()


def main():
    """main"""
    getThreads=[]
    checkThreads=[]
    getProxyFromFile(config.REGION)
    print("上次代理IP文件中共有代理：" + len(rawProxyDir))

    # 对西祠网站开启一个线程负责抓取代理
    for i in range(len(XC_targets)):
        p_city = XC_cityCompileMap[config.REGION]
        print p_city
        t_city = ProxyGet(XC_targets[i], p_city)
        getThreads.append(t_city)

    # 对好代理网站进行目标抓取
    for i in range(len(HDL_targets)):
        p_city = HDL_cityCompileMap[config.REGION]
        print p_city
        t_city = ProxyGet(HDL_targets[i], p_city)
        getThreads.append(t_city)

    for i in range(len(getThreads)):
        getThreads[i].start()

    for i in range(len(getThreads)):
        getThreads[i].join()

    print '.' * 10 + "总共抓取了%s个代理" % len(rawProxyDir) + '.' * 10

    TIME_FORMAT = '%Y%m%d_%H'
    # today = datetime.date.today()

    if not os.path.isdir("proxyList/" + config.REGION):
        print "makedirs: proxyList/" + config.REGION
        os.makedirs("proxyList/" + config.REGION)

    # 此处windows处路径为\,若转为Linux下服务，可能需要修改
    fileBeforePath = "proxyList/" + config.REGION + "/proxyListRaw." + time.strftime(TIME_FORMAT)
    fileAfterPath = "proxyList/" + config.REGION + "/proxyListAfter." + time.strftime(TIME_FORMAT)
    #持久化验证前的数据
    fileBefore = open(fileBeforePath, 'w+')
    for proxy in sorted(rawProxyDir.values(), cmp = lambda x, y: cmp(x[3], y[3])):
        print "write raw proxy is: %s\t%s\t%s\t%s" % (proxy[0], proxy[1], proxy[2], proxy[3])
        fileBefore.write("%s\t%s\t%s\t%s\n" % (proxy[0], proxy[1], proxy[2], proxy[3]))
    fileBefore.close()


    #开启20个线程负责校验，将抓取到的代理分成20份，每个线程校验一份
    for i in range(20):
        t = ProxyCheck(rawProxyDir.values()[((len(rawProxyDir.values()) + 19) / 20)\
                * i: ((len(rawProxyDir.values()) + 19) / 20) * (i + 1)])
        checkThreads.append(t)

    for i in range(len(checkThreads)):
        checkThreads[i].start()

    for i in range(len(checkThreads)):
        checkThreads[i].join()

    print '.' * 10 + "总共有%s个代理通过校验" % len(checkedProxyList) + '.' * 10

    #持久化验证后的数据
    fileAfter = open(fileAfterPath, 'w+')
    for proxy in sorted(checkedProxyList.values(), cmp = lambda x, y: cmp(x[4], y[4])):
        print "checked proxy is: %s\t%s\t%s\t%s" % (proxy[0], proxy[1], proxy[2], proxy[4])
        fileAfter.write("%s\t%s\t%s\t%s\n" % (proxy[0], proxy[1], proxy[2], proxy[4]))
    fileAfter.close()


if __name__ == "__main__":
    main()
    # currentIP = ipProxy.getIpFromRegion()
