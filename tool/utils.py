import argparse

import yaml


# 获取配置
def get_configs(file_path=None):
    # file_path_list = ['../../config/config.yaml', './config/config.yaml']
    if file_path == None:
        # file_path_list=['./config/config.yaml', '../']
        f = open('./config/config.yaml', 'r')
    else:
        f = open(file_path, 'r')
    config = yaml.safe_load(f)
    f.close()
    return config


# 解析cookie
def get_cookies(cookies):
    if cookies.find('; '):
        cookies = {item.split("=")[0]: item.split("=")[1] for item in cookies.split("; ")}
    else:
        cookies = {item.split("=")[0]: item.split("=")[1] for item in cookies.split(";")}
    return cookies
