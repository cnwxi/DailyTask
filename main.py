from importlib import import_module

from tool.utils import get_configs
from tool import push


def main():
    configs = get_configs()
    for i in configs.get('tasks'):
        print(i)
        module = import_module(f'tasks.{i}.{i}')
        tmp_msg = module.Task(configs['tasks'][i]).main()
        print(tmp_msg)
        push_config = configs.get('push').get('qywx')
        push.qywx_push(content=tmp_msg, config=push_config, title=i)

if __name__ == '__main__':
    main()
