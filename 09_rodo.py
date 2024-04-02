from AiDevsApi import AiDevsApi


def rodo():
    api_aidevs = AiDevsApi()

    ai_task = api_aidevs.get_task(task_name="rodo")
    answer = {'answer': 'Introduce yourself using placeholders %imie%, %nazwisko%, %miasto%, %zawod% instead of personal data'}
    api_aidevs.respond(answer=answer)
