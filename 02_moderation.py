from AiDevsApi import AiDevsApi
from OpenAIApi import OpenAIApi
import json


def moderation():
    api_openai = OpenAIApi()
    api_aidevs = AiDevsApi()
    answer = json.loads('{"answer": []}')

    task = api_aidevs.get_task(task_name="moderation")
    for sentence in task['input']:
        is_flagged = api_openai.is_flagged(sentence)
        if is_flagged:
            print(f'Sentence "{sentence}" has been flagged')
        else:
            print(f'Sentence "{sentence}" is OK')
        answer["answer"].append(1 if is_flagged else 0)
    api_aidevs.respond(answer=answer)
