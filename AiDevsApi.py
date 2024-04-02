import requests
import time
import json
import os


class AiDevsApi:
    def __init__(self):
        self._api_key = os.environ['AI_DEVS_KEY']
        self.token = None
        self.time = None

    def authorize(self, task_name='helloapi'):
        task_name = task_name.lower()
        r = requests.post('https://tasks.aidevs.pl/token/' + task_name,
                          data='{"apikey":"' + self._api_key + '"}')
        if r.json()['code'] != 0:
            print(f"[Error] Authorization failed, code \"{r.json()['code']}\"")
            print(f"[Error] Message: \"{r.json()}\"")
            exit(1)
        else:
            print(f"Token fetched: \"{r.json()}\"")
            self.token = r.json()['token']
            self.time = time.time()

    def get_task(self, task_name=None):
        if not self.token:
            if not task_name:
                print(f"[Error] Not authorized, and cannot do it without task_name")
                exit(2)
            self.authorize(task_name)
        r = requests.get('https://tasks.aidevs.pl/task/' + self.token)
        if r.json()['code'] != 0:
            print(f"[Error] Code {r.json()['msg']}")
            exit(3)
        else:
            print(f"Task fetched: \"{r.json()}\"")
            return r.json()

    def send(self, params):
        files = {'file': open('file.txt', 'w+b')}
        r = requests.post('https://tasks.aidevs.pl/task/' + self.token,
                          files=files,
                          data=params)
        print(f"Sent POST with params: \"{params}\"")
        print(f"Response collected: \"{r.json()}\"")
        if r.json()['code'] != 0:
            print(f"[Error] Code {r.json()['code']}")
            print(f"[Error] Why: {r.json()['msg']}")
        return r.json()

    def respond(self, answer, task_name=None):
        if not self.token:
            self.get_task(task_name)
        if not self.time or time.time() - self.time > 120:
            print(f"[WARNING] Task timeout, re-authorization")
            self.get_task(task_name)
        r = requests.post('https://tasks.aidevs.pl/answer/' + self.token,
                          data=json.dumps(answer))
        print(f"Sent answer: \"{answer}\"")
        print(f"Response collected: \"{r.json()}\"")
        if r.json()['code'] != 0:
            print(f"[Error] Code {r.json()['code']}")
            print(f"[Error] What: {r.json()['msg']}")
        return r.json()['code']


def nested_set(dic, keys, value):
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value
