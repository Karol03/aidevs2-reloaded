from AiDevsApi import AiDevsApi
import os


def ownapi():
    api_aidevs = AiDevsApi()

    task = api_aidevs.get_task(task_name="ownapi")

    #
    # URL to make.com webhook
    # Scenario structure:
    # Webhook -> OpenAI (Create a completion) -> Create JSON -> Webhook (response)
    #
    api_aidevs.respond(answer={"answer": os.environ['API_URL']})
