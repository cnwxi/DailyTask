from importlib import import_module

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

def check_config(config):
    for i in config:
        if i is not None and 'your' not in config[i]:
            return True
        else:
            return False


def run_task(task,task_config):
    module = import_module(f'tasks.{task}.{task}')
    tmp_msg = module.Task(task_config=task_config).main()
    return tmp_msg