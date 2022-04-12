from tool.utils import get_configs, check_config, run_task
from tool.push import push


def main():
    configs = get_configs()
    task_configs = configs.get('tasks')
    push_configs = configs.get('push')
    msg = []
    for task in task_configs:
        print(task)
        task_config = task_configs[task]
        if not check_config(task_config):
            print(f'{task}-配置文件未修改')
            continue
        tmp_msg = run_task(task, task_config)
        print(tmp_msg)
        msg.append([task, tmp_msg])
    for task, tmp_msg in msg:
        push(push_configs, tmp_msg, task)


if __name__ == '__main__':
    main()
