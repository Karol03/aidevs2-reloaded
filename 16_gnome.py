from AiDevsApi import AiDevsApi
from OpenAIApi import OpenAIApi


def gnome():
    api_openai = OpenAIApi()
    api_aidevs = AiDevsApi()

    task = api_aidevs.get_task(task_name="gnome")
    response = api_openai.vision(prompt="If the picture presents gnome with a hat on the head, write the hat color "
                                        "in polish otherwise respond 'No'\n."
                                        "Be short and precise, don't add any other comments only "
                                        "color in polish or 'No'",
                                 image_path=task['url'])
    if response.lower() == "no":
        api_aidevs.respond(answer={"answer": "error"})
    else:
        api_aidevs.respond(answer={"answer": response.lower()})
