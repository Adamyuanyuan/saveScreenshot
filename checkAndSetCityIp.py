# -*- coding:  utf-8 -*-
#!/usr/bin/python
# author: wangxiaogang02@baidu.com
'''
代理IP维护策略：
----与城市设定解耦，只与维护的IP列表文件的IP值有关，此脚本只管IP可用性，不管城市
每一个小时从各种代理IP网站抓取对应城市的代理IP，这些IP是逐渐累积的，按时间保存在ProxyList文件夹下：
每15分钟，从cityIp.cfg中读取验证维护两个可用的IP：
1. 如果都可用，则不变
2. 如果只有一个IP可用，则使可用的IP为ip1，更新ip2(从维护的IP文件中读取并验证)
3. 如果两个IP都不可用，则从维护的IP列表中找出两个IP(这里需要知道来自IP列表的行数)，并验证
4. 如果列表中找不出可用的IP，则循环驱动例行的grapCityIp.py提前执行，直到找到可用IP
5. 如果驱动grapCityIp.py执行超过3次，则取消代理，如果超过5次，则暂停循环，代表本次行动失败
todo: 并发送邮件给我
'''

import ConfigParser
import ipProxy
import urllib2
import time
import config
import datetime
import os
import subprocess
import sys

CONFIGFILE="cityIp.cfg"


def makePath(pathDir):
    """如果目录不存在，则创建目录"""
    if not os.path.exists(pathDir):
        print(pathDir + "path not exists and create it")
        os.makedirs(pathDir)


def initLog():
    """为server配置log"""
    import logging
    logger = logging.getLogger()
    DATE_FORMAT = '%Y%m%d'
    currentDate = datetime.datetime.now().strftime(DATE_FORMAT)
    makePath("logs/checkAndSetIpLog")
    logFileName = "logs/checkAndSetIpLog/checkAndSetIp_" + currentDate + ".log"
    hdlr = logging.basicConfig(filename = logFileName,
            level = logging.NOTSET, format = '%(asctime)s %(levelname)s: %(message)s')
    return logger

logger = initLog()

def checkProxy(proxy):
    """检查Proxy逻辑"""
    testUrl = "https://www.sogou.com/"
    testStr = "050897"
    # testStr = "050897"
    # testUrl = "https://www.baidu.com/"
    # testStr = "030173"
    timeout = 3
    cookies = urllib2.HTTPCookieProcessor()
    proxyHandler = urllib2.ProxyHandler({"http": r'http://%s' % (proxy)})
    opener = urllib2.build_opener(cookies, proxyHandler, urllib2.HTTPHandler)
    r = urllib2.Request(testUrl)
    r.add_header("Accept-Language","utf-8") #加入头信息,这样可避免403错误
    r.add_header("Content-Type","text/html; charset=utf-8")
    r.add_header("User-Agent","Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.1.4322)")
    # opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) \
    #             AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36')]
    t1 = time.time()
    try:
        req = opener.open(r, timeout = timeout)
        result = req.read()
        # print(result)
        timeused = time.time() - t1
        pos = result.find(testStr)

        if pos > 1:
            logger.info("ip ok: " + proxy)
            print("ip ok: " + proxy)
            return True
        else:
            logger.info("ip not use: " + proxy)
            print("ip not use: " + proxy)
            return False
    except Exception as e:
        return False


def getIpfromProxyList(exceptIp):
    """从每小时轮询一次的IP文件中获得最好的代理IP"""
    logger.info("getIpfromProxyList start")

    TIME_FORMAT = '%Y%m%d_%H'
    currentHour = datetime.datetime.now()
    lastHour = currentHour - datetime.timedelta(hours = 1)
    fileAfterPath = "proxyList/" + config.REGION + "/proxyListAfter." \
            + currentHour.strftime(TIME_FORMAT)
    if not os.path.exists(fileAfterPath):
        logger.info("Use last hour proxy list")
        print("Use last hour proxy list")
        fileAfterPath = "proxyList/" + config.REGION + "/proxyListAfter." \
                + lastHour.strftime(TIME_FORMAT)

    if not os.path.exists(fileAfterPath):
        logger.info("last hour proxy list dose not exists, return 0")
        print("last hour proxy list dose not exists, return 0")
        return "0"

    try:    
        readFile = open(fileAfterPath, "r")
        
        for eachLine in readFile:
            lineArray = eachLine.split('\t')
            if (lineArray[0] != exceptIp) and checkProxy(lineArray[0]):
                print(lineArray[0])
                return lineArray[0]

        return "0"
    except Exception as e:
        print("ERROR: " + str(e.args))
        return "0"
    finally:
        readFile.close()


def main():
    """main"""
    logger.info("------------start--------------")
    config = ConfigParser.ConfigParser()
    config.read(CONFIGFILE)

    ip1 = config.get("info", "ip1")
    ip2 = config.get("info", "ip2")
    logger.info(ip1)
    print(ip1)
    logger.info(ip2)
    print(ip2)
    if checkProxy(ip1):
        ipProxy.setProxy(ip1)
        if checkProxy(ip2):
            logger.info("ip1 and ip2 ok")
            print("ip1 and ip2 ok")
            return
        else:
            logger.info("ip2 need selectedIp")
            print("ip2 need selectedIp")
            # 从IP列表中找到IP不是ip1的IP并验证
            selectedIp = getIpfromProxyList(ip1)
            config.set("info", "ip2", selectedIp)
            config.write(open(CONFIGFILE, "w"))
            return

    else:
        if checkProxy(ip2):
            logger.info("ip2 --> ip1")
            print("ip2 --> ip1")
            ipProxy.setProxy(ip2)
            selectedIp = getIpfromProxyList(ip2)
            config.set("info", "ip1", ip2)
            config.set("info", "ip2", selectedIp)
            config.write(open(CONFIGFILE, "w"))
            return

        # 如果两个IP都不可用，查找之后的ip仍然不可用，则驱动例行的grapCityIp.py提前执行
        else:
            logger.info("ip1 and ip2 all need selectedIp")
            print("ip1 and ip2 all need selectedIp")
            selectedIp1 = getIpfromProxyList("0")
            # 一直循环驱动直到找到正确IP
            loopVar = 0
            while selectedIp1 == "0":
                if loopVar < 3:
                    loopVar += 1
                elif loopVar < 5:
                    loopVar += 1
                    # 如果超过三次还不成功，则取消代理
                    ipProxy.setProxy("0")
                else:
                    return

                grapCityIpScript = "python grapCityIp.py"
                scriptResult = subprocess.call(grapCityIpScript.encode(\
                            sys.getfilesystemencoding()))
                logger.info(scriptResult)
                selectedIp1 = getIpfromProxyList("0")

            ipProxy.setProxy(selectedIp1)
            selectedIp2 = getIpfromProxyList(selectedIp1)
            config.set("info", "ip1", selectedIp1)
            config.set("info", "ip2", selectedIp2)
            config.write(open(CONFIGFILE, "w"))
            return

if __name__ == "__main__":
    main()
