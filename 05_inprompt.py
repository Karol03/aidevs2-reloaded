from AiDevsApi import AiDevsApi
from OpenAIApi import OpenAIApi


def inprompt():
    api_openai = OpenAIApi()
    api_aidevs = AiDevsApi()

    ai_task = api_aidevs.get_task(task_name="inprompt")
    sentences = ai_task["input"]
    question = ai_task["question"]

    system = """
    Dla podanego zdania wypisz imię osoby, której zdanie dotyczy.
    Wypisuj tylko imię bez żadnych innych znaków."""
    names = api_openai.multiple_chat(prompts=sentences, system=system, max_concurrent=5)
    whom = api_openai.chat(prompt=question, system=system)

    facts = [sentences[i] for i, name in enumerate(names) if name == whom]
    facts = '\n\n'.join(facts)
    print(f"Prepared facts for {whom}:\n###\n{facts}\n###")

    system = f"""
    Odpowiadaj na polecenia użytkownika tylko posługując się faktami. Mów bardzo zwięźle i precyzyjnie. Gdy nie
    jesteś w stanie odpowiedzieć, mów 'Nie wiem'.  
    
    Fakty:
    {facts}
    """
    answer = {'answer': api_openai.chat(system=system, prompt=question)}
    api_aidevs.respond(answer=answer)
