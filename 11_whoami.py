from AiDevsApi import AiDevsApi
from OpenAIApi import OpenAIApi
import re


def whoami():
    api_openai = OpenAIApi()
    api_aidevs = AiDevsApi()

    retries = 0
    max_retries = 12

    hints = []

    while retries < max_retries:
        retries += 1

        api_aidevs.authorize(task_name="whoami")
        ai_task = api_aidevs.get_task()

        if ai_task['hint'] in hints:
            continue

        hints.append(ai_task['hint'])
        formatted_hints = '\n'.join('-{}' for _ in range(len(hints))).format(*hints)

        system = f"""
Korzystając z faktów dostarczonych przez użytkownika odpowiadam na pytanie kim była owa postać.
Jeśli nie mogę stwierdzić jednoznacznie kim była postać odpowiadam '...'
Moje odpowiedzi są bardzo zwięzłe, nie dodaję żadnych komentarzy. 

Przykład```
U: był wojownikiem
A: ...
```"""

        prompt = f"Fakty o postaci:\n{formatted_hints}\n\nNazwa postaci, albo '...'"

        answer = api_openai.chat(prompt=prompt, system=system)
        if re.search(pattern='^([a-zA-Z\\ ])+$', string=answer):
            api_aidevs.authorize(task_name="whoami")
            api_aidevs.respond(answer={'answer': answer})
            break

    if retries >= max_retries:
        print(f"[FAILED] Hit the max retries of {max_retries}, no respond has been sent back")
        exit(10)
