from AiDevsApi import AiDevsApi


def functions():
    api_aidevs = AiDevsApi()

    ai_task = api_aidevs.get_task(task_name="functions")

    answer = {}
    answer['name'] = "addUser"
    answer['description'] = "Adds a new user"
    answer['parameters'] = {}
    answer['parameters']['type'] = 'object'
    answer['parameters']['properties'] = {}
    answer['parameters']['properties']['name'] = {"type": "string", "description": "user's name"}
    answer['parameters']['properties']['surname'] = {"type": "string", "description": "user's surname"}
    answer['parameters']['properties']['year'] = {"type": "integer", "description": "user's year of born"}
    answer = {'answer': answer}
    api_aidevs.respond(answer=answer)
