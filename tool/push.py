import requests
import json
from tool.utils import check_config
from importlib import import_module


def push(configs, content, title):
    if configs is None:
        print('未配置推送')
        return
    for push in configs:
        push_config = configs.get(push)
        if check_config(push_config):
            module = import_module('tool.push')
            func = getattr(module, push)
            func(push_config, content, title)
        else:
            print(f'{push} 推送配置文件未修改')
            continue


def server(config, content, title):
    print(f"server 酱推送 {title}任务结果")
    data = {"text": "每日签到", "desp": content.replace("\n", "\n\n")}
    requests.post(url=f"https://sc.ftqq.com/{config.get('sendkey')}.send", data=data)
    return


def qywx(config, content, title):
    print(f'企业微信推送 {title}任务结果')
    qywx_corpid = config.get('corp_id')
    qywx_agentid = config.get('agent_id')
    qywx_corpsecret = config.get('corp_secret')
    qywx_touser = config.get('touser')
    res = requests.get(
        f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={qywx_corpid}&corpsecret={qywx_corpsecret}"
    )
    token = res.json().get("access_token", False)
    if config.get('type') == 'textcard':
        data = {
            "touser": qywx_touser,
            "agentid": int(qywx_agentid),
            "msgtype": "textcard",
            "textcard": {
                "title": title,
                "description": content,
                "url": "URL",
            },
        }
    else:
        data = {
            "touser": qywx_touser,
            "agentid": int(qywx_agentid),
            "msgtype": "text",
            "text": {
                "content": title + '\n' + content,
            },
        }
    requests.post(url=f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}", data=json.dumps(data))
    return


def bark(config, content, title):
    print(f'Bark推送 {title}任务结果')
    url = config.get('url')
    if not url.endswith("/"):
        url += "/"
    url = f"{url}{content}"
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    requests.get(url=url, headers=headers)
    return


def telegram(config, content, title):
    print(f'Telegram推送 {title}任务结果')
    api_host = config.get('api_host')
    proxy = config.get('proxy')
    bot_token = config.get('bot_token')
    user_id = config.get('user_id')
    send_data = {"chat_id": user_id, "text": content, "disable_web_page_preview": "true"}
    if api_host:
        url = f"https://{api_host}/bot{bot_token}/sendMessage"
    else:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    if proxy:
        proxies = {
            "http": proxy,
            "https": proxy,
        }
    else:
        proxies = None
    requests.post(url=url, data=send_data, proxies=proxies)
    return
