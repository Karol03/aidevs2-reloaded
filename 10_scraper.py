from AiDevsApi import AiDevsApi
from OpenAIApi import OpenAIApi
import requests
import time


def scraper():
    api_openai = OpenAIApi()
    api_aidevs = AiDevsApi()

    max_tries = 6
    tries = 0

    while tries < max_tries:
        ai_task = api_aidevs.get_task(task_name="scraper")

        task = ai_task['msg']
        prompt = ai_task['question']
        web_address = ai_task['input']

        content = requests.get(web_address,
                               timeout=30,
                               headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0'
        })
        if content.status_code != 200:
            print(f"Scraper failed to get page content, code = {content.status_code}")
            print(f"What: {content.content}")
            tries += 1
            time.sleep(2 ** (tries - 1))
            continue
        context = content.text

        system = f"""
        Based on context below, respond the the user question. Respond ultra-briefly.
        
        {task}
        
        context```
        {context}
        ```
        """

        response = api_openai.chat(prompt=prompt, system=system)
        answer = {'answer': response}
        api_aidevs.respond(answer=answer)
        break

    if tries >= max_tries:
        print(f"[FAILED] Hit the max tries of {max_tries}, no respond has been sent back")
        exit(10)
