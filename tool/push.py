import requests
import json


def qywx_push(content, config, title):
    print(f'推送{title}任务结果')
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
