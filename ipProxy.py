# -*- coding:  utf-8 -*-
''' 设定代理IP相关的方法

Authors: wangxiaogang02@baidu.com
Date: 2015/08/07
'''

import io
import sys
import time
import re
import os
import _winreg
import datetime

def getIpFromRegion(region):
    """通过地区字符串来得到对应的代理IP"""
    if (region == '') or (region == 'shanghai') or ("上海" in region):
        print("region is shanghai")
        return '0'
    else:
        try:
            TIME_FORMAT = '%Y%m%d_%H'
            currentHour = datetime.datetime.now()
            lastHour = currentHour - datetime.timedelta(hours = 1)
            fileAfterPath = "proxyList/all/proxyListAfter." \
                    + currentHour.strftime(TIME_FORMAT)
            if not os.path.exists(fileAfterPath):
                print("Use last hour proxy list")
                fileAfterPath = "proxyList/all/proxyListAfter." \
                        + lastHour.strftime(TIME_FORMAT)
            
            readFile = open(fileAfterPath, "r")
            
            for eachLine in readFile:
                lineArray = eachLine.split('\t')
                if region in eachLine:
                    readFile.close()
                    print(lineArray[0])
                    return lineArray[0]
            return 'IpNotFonud'
        except Exception as e:
            print("ERROR: " + str(e.args))
        finally:
            readFile.close()


def enableProxy(proxy):
    """通过修改windows注册列表并且刷新使得IP有效"""
    xpath = "Software\Microsoft\Windows\CurrentVersion\Internet Settings"
    try:
        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, xpath, 0, _winreg.KEY_WRITE)
        _winreg.SetValueEx(key, "ProxyEnable", 0, _winreg.REG_DWORD, 1)
        _winreg.SetValueEx(key, "ProxyServer", 0, _winreg.REG_SZ, proxy)
    except Exception as e:
        print("ERROR: " + str(e.args))
    finally:
        None


def disableProxy():
    """通过修改windows注册列表并且刷新使得IP无效"""
    proxy = ""
    xpath = "Software\Microsoft\Windows\CurrentVersion\Internet Settings"
    try:
        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, xpath, 0, _winreg.KEY_WRITE)
        _winreg.SetValueEx(key, "ProxyEnable", 0, _winreg.REG_DWORD, 0)
        _winreg.SetValueEx(key, "ProxyServer", 0, _winreg.REG_SZ, proxy)
    except Exception as e:
        print("ERROR: " + str(e.args))
    finally:
        None


def refresh():
    """刷新使得注册表的改变生效，就不需要重启IE了"""
    import ctypes

    INTERNET_OPTION_REFRESH = 37
    INTERNET_OPTION_SETTINGS_CHANGED = 39

    internet_set_option = ctypes.windll.Wininet.InternetSetOptionW

    internet_set_option(0, INTERNET_OPTION_REFRESH, 0, 0)
    internet_set_option(0, INTERNET_OPTION_SETTINGS_CHANGED, 0, 0)


def setProxy(proxy):
    """设定IP"""
    if proxy == "0":
        try:
            disableProxy()
            refresh()
            print("disableProxy")
        except Exception as e:
            print("ERROR: " + str(e.args))
        finally:
            pass
    else:
        try:
            print("set property: " + proxy)
            disableProxy()
            enableProxy(proxy)
            refresh()
        except Exception as e:
            print("ERROR: " + str(e.args))
        finally:
            pass


def main():
    """main函数,求CR"""
    proxy = sys.argv[1]
    setProxy(proxy)

if __name__ == '__main__':
    main()