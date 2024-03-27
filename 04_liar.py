from AiDevsApi import AiDevsApi
from OpenAIApi import OpenAIApi


def liar():
    api_openai = OpenAIApi()
    api_aidevs = AiDevsApi()

    query = "Where the hedgehog stamps at night?"
    api_aidevs.authorize(task_name="liar")
    ai_answer = api_aidevs.send({'question': query})

    system = """
I am a very insightful analyzer. I only use 'YES' and 'NO' in a conversation.

I get a conversation piece in the format
Q: <query>
A: <answer>.

If 'A' is thematically related to 'Q' I answer 'YES' in other cases I answer 'NO'.
    """
    answer = api_openai.chat(system=system, prompt=f"""
Q: {query}
A: {ai_answer['answer']}
""")
    answer = {'answer': answer}
    api_aidevs.respond(answer=answer)
