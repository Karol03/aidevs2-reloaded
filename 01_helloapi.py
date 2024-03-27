from AiDevsApi import AiDevsApi
import json


def helloapi():
    api = AiDevsApi()
    answer = json.loads('{}')

    task = api.get_task(task_name="helloapi")
    answer["answer"] = task["cookie"]
    api.respond(answer=answer)
