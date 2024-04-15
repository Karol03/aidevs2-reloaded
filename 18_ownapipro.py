from AiDevsApi import AiDevsApi
import os


def ownapipro():
    api_aidevs = AiDevsApi()

    task = api_aidevs.get_task(task_name="ownapipro")

    #
    # URL to make.com webhook
    #
    api_aidevs.respond(answer={"answer": os.environ['MAKE_API_URL']})
