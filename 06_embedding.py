from AiDevsApi import AiDevsApi
from OpenAIApi import OpenAIApi


def embedding():
    api_openai = OpenAIApi()
    api_aidevs = AiDevsApi()

    ai_task = api_aidevs.get_task(task_name="embedding")
    embeddings_array = api_openai.embeddings(content="Hawaiian pizza")
    answer = {"answer": embeddings_array}
    api_aidevs.respond(answer=answer)
