#coding=utf-8
"""
    SendDataClient类，作为flashshot的服务
"""
import os
import requests
import logging
import sys


TARGET_SERVER_ADDR = 'http://10.48.48.62:8089'
TARGET_FILE_TYPE = '.png'
logger = None

def init_logger():
    """
    日志
    """
    global logger
    log_file = 'log.txt'
    logger = logging.getLogger()
    file_hdl = logging.FileHandler(log_file)
    stream_hdl = logging.StreamHandler()
    fmt = logging.Formatter(
        '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    file_hdl.setFormatter(fmt)
    stream_hdl.setFormatter(fmt)
    logger.addHandler(file_hdl)
    logger.addHandler(stream_hdl)
    logger.setLevel(logging.INFO)


def upload_files(target_folder, target_filenames):
    """
    上传文件
    """
    cur_path = os.getcwd()    

    for file_name in target_filenames:
        full_file_name = os.path.join(
            cur_path, target_folder, file_name)
        logger.info('send: {v}'.format(v=full_file_name))
        file_content = {'file': open(full_file_name, 'rb')}
        
        try:
            response = requests.post(
                TARGET_SERVER_ADDR, files=file_content)
            logger.info('response: {v0}, {v1}'.format(
                v0=response.url, v1=response.text))
        except Exception as e:
            logger.error('send faild: {v}'.format(v=e))


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
                logger.info('file: {v} found'.format(v=each_file))
    else:
        logger.error('target folder {v} do not exist'.format(v=target_folder))

    if len(target_filenames) == 0:
        logger.info('no target file found')
    return target_filenames


def main():
    """
    SendDataClient类，作为flashshot的服务
    """
    init_logger()    
    target_folder = sys.argv[1]
    target_filenames = get_file_list(target_folder)
    upload_files(target_folder, target_filenames)  

if __name__ == '__main__':
    main()

