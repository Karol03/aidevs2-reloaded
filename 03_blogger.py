from AiDevsApi import AiDevsApi
from OpenAIApi import OpenAIApi
import json


def blogger():
    api_openai = OpenAIApi()
    api_aidevs = AiDevsApi()

    system = "Jestem znanym blogerem z dużą wiedzą, lubię pisać długie teksty na zadane tematy," \
             "zawsze podążam za wskazówkami.\n\n" \
             "###Wskazówki\n" \
             "Napisz wpis na bloga na temat przyrządzania pizzy Margherity." \
             "Jako wejście otrzymasz spis 4 rozdziałów, które muszą pojawić się we wpisie." \
             "Jako odpowiedź musisz zwrócić tablicę (w formacie JSON) złożoną z 4 pól reprezentujących te" \
             "cztery napisane rozdziały," \
             "np.: {\"answer\":[\"tekst 1\",\"tekst 2\",\"tekst 3\",\"tekst 4\"]}"

    task = api_aidevs.get_task(task_name="blogger")
    prompt = '\', \''.join(task['blog'])
    answer = api_openai.chat(system=system, prompt=prompt)
    answer = json.loads(answer)
    api_aidevs.respond(answer=answer)
