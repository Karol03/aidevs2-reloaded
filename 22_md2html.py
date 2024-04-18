from AiDevsApi import AiDevsApi
from OpenAIApi import OpenAIApi


def md2html():
    api_aidevs = AiDevsApi()
    openai = OpenAIApi()

    # openai.upload_file("ft_md2html.jsonl")
    # if uploaded go to https://platform.openai.com/finetune
    # and use the file to create a fine tuned model

    system = "md2html"

    openai = OpenAIApi(model="ft:gpt-3.5-turbo-0125:personal::9FH6VOMq",
                       temperature=0)

    task = api_aidevs.get_task(task_name="md2html")
    response = openai.chat(prompt=task["input"], system=system)

    api_aidevs.respond(answer={"answer": response})
