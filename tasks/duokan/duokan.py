# -*- coding: utf-8 -*-
import time

import requests

from tasks.duokan.code_list import code_list, gift_code_list
from tool.utils import get_cookies, get_configs


class Task:
    name = "多看阅读"

    def __init__(self, task_config):
        self.config = task_config
        self.get_free = self.config.get('get_free')
        self.more_task = self.config.get('more_task')
        self.gift_code_list = gift_code_list
        self.code_list = code_list
        self.headers = {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"}

    def get_data(self, cookies):
        device_id = cookies.get("device_id")
        t = int(time.time())
        t_device_id = f"{device_id}&{t}"
        c = 0
        for index, one in enumerate(t_device_id):
            c = (c * 131 + ord(one)) % 65536
        data = f"_t={t}&_c={c}"
        return data

    def sign(self, cookies):
        url = "https://www.duokan.com/checkin/v0/checkin"
        data = self.get_data(cookies=cookies)
        response = requests.post(url=url, data=data, cookies=cookies, headers=self.headers)
        result = response.json()
        msg = {"name": "每日签到", "value": result.get("msg")}
        return msg

    # 有改动
    def delay(self, cookies, date):
        url = "https://www.duokan.com/store/v0/award/coin/delay"
        data = f"date={date}&{self.get_data(cookies=cookies)}&withid=1"
        ret = requests.post(url=url, data=data, cookies=cookies, headers=self.headers).json()
        return ret

    # 有改动
    def info(self, cookies):
        url = "https://www.duokan.com/store/v0/award/coin/list"
        data = f"sandbox=0&{self.get_data(cookies=cookies)}&withid=1"
        response = requests.post(url=url, data=data, cookies=cookies, headers=self.headers)
        result = response.json()
        msg = []
        if "尚未登录" not in result.get("msg"):
            coin = sum([one.get("coin") for one in result.get("data", {}).get("award")])
            msg.append({"name": "当前书豆", "value": coin})
            for one in result.get("data", {}).get("award"):
                if one.get("delay") == 1:
                    ret = self.delay(cookies, one.get('expire'))
                    msg.append(
                        {"name": f"{one.get('expire')} 到期", "value": f"{one.get('coin')} 书豆 | 延期：{ret.get('msg')}"})
                else:
                    msg.append({"name": f"{one.get('expire')} 到期", "value": f"{one.get('coin')} 书豆"})
            return msg
        else:
            return [{"name": "账号异常", "value": "Cookie 失效"}]

    def free(self, cookies):
        if self.get_free:
            url = "https://www.duokan.com/hs/v4/channel/query/2027"
            response = requests.get(url=url, cookies=cookies, headers=self.headers)
            bid = response.json().get("items")[0].get("data").get("book_id")
            data = f"payment_name=BC&ch=VSZUVB&book_id={bid}&price=0&allow_discount=1"
            free_url = "https://www.duokan.com/store/v0/payment/book/create"
            response = requests.post(url=free_url, data=data, cookies=cookies, headers=self.headers)
            result = response.json()
            if "尚未登录" not in result.get("msg"):
                book_title = result.get("book").get("title")
                book_msg = result.get("msg")
                msg = {"name": "今日限免", "value": f"{book_title} · {book_msg}"}
            else:
                msg = {"name": "今日限免", "value": f"Cookie 失效"}
        else:
            msg = {"name": "今日限免", "value": f"未启用"}
        return msg

    def gift(self, cookies):
        url = "https://www.duokan.com/events/common_task_gift_check"
        data = f"code=KYKJF7LL0G&{self.get_data(cookies=cookies)}&withid=1"
        response = requests.post(url=url, data=data, cookies=cookies, headers=self.headers)
        result = response.json()
        # print(result.get("chances"))
        if result.get("chances") == 20:
            msg = {"name": "体验任务", "value": "已经做完啦"}
        elif result.get("chances"):
            num = 0
            for gift_code in self.gift_code_list:
                url = "https://www.duokan.com/events/common_task_gift"
                data = f"code=KYKJF7LL0G&chances=1&sign={gift_code}&{self.get_data(cookies=cookies)}&withid=1"
                response = requests.post(url=url, data=data, cookies=cookies, headers=self.headers)
                result = response.json()
                if result.get("msg") == "成功":
                    num += 30
                    print("体验任务完成啦！豆子 +30")
                else:
                    # print(result.get("data"))
                    continue
            msg = {"name": "体验任务", "value": f"获得 {num} 豆子"}
        else:
            msg = {"name": "体验任务", "value": f"{response.text}"}
        return msg

    def add_draw(self, cookies):
        success_count = 0
        for one in range(6):
            url = "https://www.duokan.com/store/v0/event/chances/add"
            data = f"code=8ulcky4bknbe_f&count=1&{self.get_data(cookies=cookies)}&withid=1"
            response = requests.post(url=url, data=data, cookies=cookies, headers=self.headers)
            result = response.json()
            if result.get("result") == 0:
                success_count += 1
        msg = {"name": "添加抽奖", "value": f"{success_count} 次"}
        return msg

    def draw(self, cookies):
        success_count = 0
        for one in range(6):
            url = "https://www.duokan.com/store/v0/event/drawing"
            data = f"code=8ulcky4bknbe_f&{self.get_data(cookies=cookies)}&withid=1"
            response = requests.post(url=url, data=data, cookies=cookies, headers=self.headers)
            result = response.json()
            if result.get("result") == 0:
                success_count += 1
        msg = {"name": "成功抽奖", "value": f"{success_count} 次"}
        return msg

    # 有改动
    def download(self, cookies):
        url = "https://www.duokan.com/events/common_task_gift"
        data = f"code=J18UK6YYAY&chances=17&{self.get_data(cookies=cookies)}&withid=1"
        count = 0
        while True:
            response = requests.post(url=url, data=data, cookies=cookies, headers=self.headers)
            result = response.json()
            if result.get("result") == 130014:
                break
            count += 1
            if not self.more_task:
                break
        msg = {"name": "下载任务", "value": f"完成 {count} 次"}
        return msg

    # 有改动
    def task(self, cookies):
        success_count = 0
        url = "https://www.duokan.com/events/tasks_gift"
        count = 3 if self.more_task else 1
        for i in range(count):
            for code in self.code_list:
                data = f"code={code}&chances=3&{self.get_data(cookies=cookies)}&withid=1"
                response = requests.post(url=url, data=data, cookies=cookies, headers=self.headers)
                result = response.json()
                if result.get("result") == 0:
                    success_count += 1
        msg = {"name": "其他任务", "value": f"完成 {success_count} 个"}
        return msg

    def main(self):
        duokan_cookie = get_cookies(self.config.get("cookies"))
        sign_msg = self.sign(cookies=duokan_cookie)
        free_msg = self.free(cookies=duokan_cookie)
        gift_msg = self.gift(cookies=duokan_cookie)
        add_draw_msg = self.add_draw(cookies=duokan_cookie)
        draw_msg = self.draw(cookies=duokan_cookie)
        download_msg = self.download(cookies=duokan_cookie)
        task_msg = self.task(cookies=duokan_cookie)
        info_msg = self.info(cookies=duokan_cookie)
        msg = [sign_msg, free_msg, gift_msg, add_draw_msg, draw_msg, download_msg, task_msg] + info_msg
        # msg = info_msg
        msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
        return msg


if __name__ == "__main__":
    config = get_configs("../../config/config.yaml")
    config = config['tasks']["duokan"]
    print(Task(task_config=config).main())
