from AiDevsApi import AiDevsApi
from OpenAIApi import OpenAIApi
import os


def google():
    api_aidevs = AiDevsApi()

    api_aidevs.get_task(task_name="google")

    #
    # URL to make.com webhook
    # Scenario
    # Webhook -> OpenAI (create a completion) -> HTTP (API Key request) -
    # -> JSON (parse) -> (Iterator -> Tools (Text Aggregation)) -> OpenAI (a completion) -> Webhooks (response)
    api_aidevs.respond(answer={"answer": os.environ['MAKE_API_GOOGLE_URL']})
