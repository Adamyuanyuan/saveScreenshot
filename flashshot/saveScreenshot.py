# -*- coding:  utf-8 -*-
#!/usr/bin/python
# author: wangxiaogang02@baidu.com

from selenium import webdriver

import io
import sys
import time
import re
import os
import _winreg
import datetime

def capture(url, save_fn):    
    browser = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver") # Get local session of firefox
    try:
        # browser.set_window_size(1200, 900)
        browser.get(url) # Load page
        # browser.execute_script("""
        # (function () {
        #     var y = 0;
        #     var step = 100;
        #     window.scroll(0, 0);

        # function f() {
        #     if (y < document.body.scrollHeight) {
        #         y += step;
        #         window.scroll(0, y);
        #         setTimeout(f, 50);
        #     } else {
        #         window.scroll(0, 0);
        #         document.title += "scroll-done";
        #     }
        # }
        # setTimeout(f, 1000);
        # })();
        # """)
        

        # for i in xrange(30):
        #     if "scroll-done" in browser.title:
        #         break
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
    url = sys.argv[1]
    save_fn = sys.argv[2]
    capture(url, save_fn)

if __name__ == '__main__':
    main()