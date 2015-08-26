# -*- coding:  utf-8 -*-
#!/usr/bin/python
"""
使用selenium打开浏览器，然后截图，被server调用，支持flash截图
Authors: wangxiaogang02(wangxiaogang02@baidu.com)
Date:    2015/08/26 17:23:06
"""
from selenium import webdriver

import io
import sys
import time
import re
import os
import _winreg
import datetime

def capture(url, save_fn):
    """使用selenium打开浏览器，然后截图"""
    browser = webdriver.Chrome(executable_path=
            "C:\Program Files (x86)\Google\Chrome\Application\chromedriver")
    try:
        # browser.set_window_size(1200, 900)
        browser.get(url) # Load page
        time.sleep(4)
        browser.save_screenshot(save_fn)
        # 退出chrome不退出驱动
        # browser.close()
        # 关闭chrome并退出驱动
    except:
        print("exception url:" + url)
    finally:
        browser.quit()


def main():
    """主函数"""
    url = sys.argv[1]
    save_fn = sys.argv[2]
    capture(url, save_fn)

if __name__ == '__main__':
    main()