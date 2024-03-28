from AiDevsApi import AiDevsApi
from OpenAIApi import OpenAIApi


def whisper():
    api_openai = OpenAIApi()
    api_aidevs = AiDevsApi()

    ai_task = api_aidevs.get_task(task_name="whisper")
    words = ai_task['msg'].split(' ')
    links = [word for word in words if word.endswith('.mp3')]

    transcription = api_openai.transcription(links[0])
    answer = {'answer': transcription}
    api_aidevs.respond(answer=answer)
