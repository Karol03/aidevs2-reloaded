from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from threading import Semaphore, Thread
import requests
import os
import re


class ConcurrentAsync:
    def __init__(self, task, max_concurrent):
        self.task = task
        self.semaphore = Semaphore(max_concurrent)
        self.results = {}

    def invoke(self, *args):
        self.results = {i: None for i in range(len(args))}
        requests = [self.request(i, *arg) for i, arg in enumerate(args)]
        for request in requests:
            request.join()
        self.results = sorted(self.results.items())
        return [result for i, result in self.results]

    def job(self, i, *args):
        with self.semaphore:
            self.results[i] = self.task(*args)
            print(f"Job {i} finished")

    def request(self, i, *args):
        thread = Thread(target=self.job, args=(i, *args))
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
        jobs = ConcurrentAsync(task=self.chat, max_concurrent=max_concurrent)
        return jobs.invoke(*[(prompt, system) for prompt in prompts])

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
            return r.json()['data'][0]['embedding']
        else:
            print(f"[ERROR][OpenAIApi] Invalid status code = {r.status_code}")
            exit(5)

    def multiple_embeddings(self, contents, model='text-embedding-ada-002', max_concurrent=5):
        jobs = ConcurrentAsync(task=self.embeddings, max_concurrent=max_concurrent)
        return jobs.invoke(*[(content, model) for content in contents])

    def transcription(self, content):
        file_path = "to_transcript.mp3"
        if re.search(pattern='^http.://.*', string=content):
            sound_raw = requests.request("GET", content)
            with open(file_path, "wb") as f:
                f.write(sound_raw.content)
        elif re.search(pattern='^([a-zA-Z]):\\\\.*', string=content):
            if not os.path.isfile(content):
                print(f"[ERROR][OpenAIApi] A transcription of a file that does not exist was requested '{content}'")
                exit(6)
            file_path = content
        else:
            print(f"[ERROR][OpenAIApi] Incorrect 'content = '{content}'' parameter, provide path or link to audio file")
            exit(7)

        files = {'file': open(file_path, 'rb')}
        r = requests.post('https://api.openai.com/v1/audio/transcriptions',
                          files=files,
                          data={'model': 'whisper-1'},
                          headers={'Authorization': f"Bearer {self.open_ai_token}"})
        print(f"[Transcription] Response received {r.json()}")
        if r.status_code == 200:
            return r.json()['text']
        else:
            print(f"[ERROR][OpenAIApi] Invalid status code = {r.status_code}")
            exit(5)

    def is_flagged(self, content):
        result = self.moderate(content=content)
        return result[0]['flagged']
