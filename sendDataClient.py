#coding=utf-8
"""
    SendDataClient类，作为flashshot的服务
"""
import os
import requests
import logging
import sys
import ipProxy
import config
import ConfigParser
import log


TARGET_SERVER_ADDR = 'http://10.48.48.62:8089'
TARGET_FILE_TYPE = '.jpg'
CONFIGFILE = "cityIp.cfg"


def upload_files(target_folder, target_filenames):
    """
    上传文件
    """
    cur_path = os.getcwd()    

    for file_name in target_filenames:
        full_file_name = os.path.join(
            cur_path, target_folder, file_name)
        logging.info('send: {v}'.format(v=full_file_name))
        file_content = {'file': open(full_file_name, 'rb')}
        
        try:
            response = requests.post(
                TARGET_SERVER_ADDR, files=file_content)
            logging.info('response: {v0}, {v1}'.format(
                v0=response.url, v1=response.text))
        except Exception as e:
            logging.error('send faild: {v}'.format(v=e))


def get_file_list(target_folder):
    """
    得到文件列表
    """
    target_filenames = []
    if os.path.exists(target_folder):
        all_files = os.listdir(target_folder)
        for each_file in all_files:
            if each_file.endswith(TARGET_FILE_TYPE):
                target_filenames.append(each_file)
                logging.info('file: {v} found'.format(v=each_file))
    else:
        logging.error('target folder {v} do not exist'.format(v=target_folder))

    if len(target_filenames) == 0:
        logging.info('no target file found')
    return target_filenames


def main():
    """
    SendDataClient类，作为flashshot的服务
    """

    log.init_log('./logs/send_data_client')

    # 如果配置文件中配置了这个地区需要设定IP代理，则在上传文件前，先将代理IP取消，然后等执行完毕后再设置上
    # 并且将 uping 设置为 1，此时每五分钟执行的checkIpProxy将不会修改此IP，上传结束后就修改回 0
    if config.NEED_PROXY:
        configFile = ConfigParser.ConfigParser()
        configFile.read(CONFIGFILE)
        configFile.set("info", "uping", 1)
        configFile.write(open(CONFIGFILE, "w"))
        logging.info('setProxy("0") ')
        # 在传送图片前，先将本地代理IP关掉
        ipProxy.setProxy("0")

    target_folder = sys.argv[1]
    target_filenames = get_file_list(target_folder)
    upload_files(target_folder, target_filenames)  
    
    # 在传送图片后，将本地代理Ip继续设定
    if config.NEED_PROXY:
        configFile = ConfigParser.ConfigParser()
        configFile.read(CONFIGFILE)
        ip1 = configFile.get("info", "ip1")
        configFile.set("info", "uping", 0)
        configFile.write(open(CONFIGFILE, "w"))
        enableProxyScript = "python ipProxy.py " + ip1
        os.popen(enableProxyScript)
        # ipProxy.setProxy(ip1)
        logging.info('setProxy ' + ip1)

if __name__ == '__main__':
    main()

