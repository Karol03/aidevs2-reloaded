from AiDevsApi import AiDevsApi
from OpenAIApi import OpenAIApi
from langchain_core.pydantic_v1 import BaseModel, Field
import time


class ToDo(BaseModel):
    """Add note or task to todo list"""

    desc: str = Field(..., description="Description of the task")

    def to_json(self):
        return {"tool": "ToDo", "desc": self.desc}


class Calendar(BaseModel):
    """Add event to the calendar if the day is given"""

    desc: str = Field(..., description="Short description of the event")
    date: str = Field(..., description=f'Today is {time.strftime("%A %Y-%m-%d")}, '
                                       f'get the date user provided in YYYY-MM-DD format. Only future dates')

    def to_json(self):
        return {"tool": "Calendar", "desc": self.desc, "date": self.date}


def tools():
    api_aidevs = AiDevsApi()
    api_openai = OpenAIApi(temperature=0)

    task = api_aidevs.get_task(task_name="tools")
    question = task["question"]

    matched_function = api_openai.function_calling(question, [ToDo, Calendar])
    if len(matched_function) == 0:
        print("[ERROR] Something went wrong none of functions matched (did you pass proper function list?)")
        exit(15)
    elif len(matched_function) > 1:
        print("[ERROR] Possibly invalid prompt, more than one function matched")
        exit(15)

    answer = matched_function[0].to_json()
    api_aidevs.respond(answer={'answer': answer})
