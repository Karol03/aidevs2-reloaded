from AiDevsApi import AiDevsApi
from OpenAIApi import OpenAIApi
import requests


def optimaldb():
    api_aidevs = AiDevsApi()
    api_openai = OpenAIApi(temperature=0)

    db = requests.get('https://tasks.aidevs.pl/data/3friends.json')
    db = db.json()

    zygfryd = db["zygfryd"]
    stefan = db["stefan"]
    ania = db["ania"]
    system = """
Extract only the key information from the sentence and provide it abbreviated in English.

Examples```
U: Podczas lokalnych akcji na rzecz zdrowia, Stefan prowadzi punkt kulinarne z hot dogami dla uczestników wydarzeń
A: Sells hot-dogs

U: Dumnie Zygfryd przedstawia swoje umiejętności w sztukach walki, którym oddaje się regularnie, ćwicząc aikido
A: Practices aikido

U: Lato w Hiszpanii spędzone przez Anię zaowocowało płynnością w języku hiszpańskim i miłością do flamenco
A: Knows Spanish. Loves flamenco
```

Skip the name. Sentence must be very short.
"""
    zygfryd = api_openai.multiple_chat(prompts=zygfryd, system=system)
    stefan = api_openai.multiple_chat(prompts=stefan, system=system)
    ania = api_openai.multiple_chat(prompts=ania, system=system)

    zygfryd = '\n'.join(zygfryd)
    stefan = '\n'.join(stefan)
    ania = '\n'.join(ania)

    json = f"""
Zygryd:
{zygfryd}

Stefan:
{stefan}

Ania:
{ania}
"""

    api_aidevs.get_task(task_name="optimaldb")
    api_aidevs.respond(answer={"answer": json})
