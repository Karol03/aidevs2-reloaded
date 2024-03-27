from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from threading import Semaphore, Thread
import requests
import os


class AsyncChat:
    def __init__(self, llm, max_concurrent):
        self.llm = llm
        self.semaphore = Semaphore(max_concurrent)
        self.results = {}

    def invoke(self, prompts, system):
        self.results = {i: None for i in range(len(prompts))}
        requests = [self.request(i, prompt, system) for i, prompt in enumerate(prompts)]
        for request in requests:
            request.join()
        self.results = sorted(self.results.items())
        return [result for i, result in self.results]

    def task(self, i, prompt, system):
        with self.semaphore:
            chain = ChatPromptTemplate.from_messages([
                ("system", "{system}"),
                ("user", "{input}")
            ]) | self.llm | StrOutputParser()
            self.results[i] = chain.invoke({
                "system": system,
                "input": prompt
            })
            print(f"Task {i} for prompt \"{prompt}\" done")

    def request(self, i, prompt, system):
        thread = Thread(target=self.task, args=(i, prompt, system))
        thread.start()
        return thread


class OpenAIApi:
    def __init__(self):
        self.open_ai_token = os.environ['OPEN_AI_KEY']
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=self.open_ai_token, max_tokens=2048)
        self.template = ChatPromptTemplate.from_messages([
            ("system", "{system}"),
            ("user", "{input}")
        ])
        self.chat_history = []

    def chat(self, prompt, system=''):
        output_parser = StrOutputParser()
        chain = self.template | self.llm | output_parser
        print(f"[OpenAIApi] Invoke chat with prompt: \"{prompt}\"")
        response = chain.invoke({
            "system": system,
            "input": prompt
        })
        print(f"[OpenAIApi] Get the response: \"{response}\"")
        return response

    def multiple_chat(self, prompts, system='', max_concurrent=5):
        chat = AsyncChat(self.llm, max_concurrent=max_concurrent)
        return chat.invoke(prompts=prompts, system=system)

    def moderate(self, content, model='text-moderation-latest'):
        r = requests.post('https://api.openai.com/v1/moderations',
                          json={'model': model, "input": content},
                          headers={'Authorization': f"Bearer {self.open_ai_token}"})
        print(f"[Moderation] Response received {r.json()}")
        if r.status_code == 200:
            return r.json()['results']
        else:
            print(f"[ERROR][OpenAIApi] Invalid status code = {r.status_code}")
            exit(5)

    def embeddings(self, content, model='text-embedding-ada-002'):
        r = requests.post('https://api.openai.com/v1/embeddings',
                          json={'model': model, "input": content},
                          headers={'Authorization': f"Bearer {self.open_ai_token}"})
        print(f"[Embeddings] Response received {r.json()}")
        if r.status_code == 200:
            return r.json()['data']
        else:
            print(f"[ERROR][OpenAIApi] Invalid status code = {r.status_code}")
            exit(5)

    def is_flagged(self, content):
        result = self.moderate(content=content)
        return result[0]['flagged']
