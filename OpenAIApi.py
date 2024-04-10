from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from threading import Semaphore, Thread
import requests
import os
import re
import base64


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
    def __init__(self, temperature=0.7):
        self.open_ai_token = os.environ['OPEN_AI_KEY']
        self.llm = ChatOpenAI(model="gpt-3.5-turbo",
                              openai_api_key=self.open_ai_token,
                              max_tokens=2048,
                              temperature=temperature)
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

    def function_calling(self, prompt, functions):
        output_parser = StrOutputParser()
        chain = self.template | self.llm | output_parser
        print(f"[OpenAIApi] Invoke function calling for: \"{functions}\"")
        llm_with_tools = self.llm.bind_tools(functions)
        tool_chain = llm_with_tools | PydanticToolsParser(tools=functions)
        result = tool_chain.invoke(prompt)
        print(f"[OpenAIApi] Get the response: \"{result}\"")
        return result

    def multiple_embeddings(self, contents, model='text-embedding-ada-002', max_concurrent=5):
        jobs = ConcurrentAsync(task=self.embeddings, max_concurrent=max_concurrent)
        return jobs.invoke(*[(content, model) for content in contents])

    def vision(self, prompt, image_path):
        image = None
        if re.search(pattern='^http.://.*', string=image_path):
            image = requests.request("GET", image_path)
            image = base64.b64encode(image.content).decode('utf-8')
        elif re.search(pattern='^([a-zA-Z]):\\\\.*', string=image_path):
            if not os.path.isfile(image_path):
                print(f"[ERROR][OpenAIApi] An image file doesn't exists, path = '{image_path}'")
                exit(6)
            with open(image_path, 'rb') as img:
                image = base64.b64encode(img.read()).decode('utf-8')
        else:
            print(f"[ERROR][OpenAIApi] Incorrect 'image_path='{image_path}'', provide system path or web link")
            exit(7)

        print(f"[OpenAIApi] Invoke chat with prompt: \"{prompt}\"")
        content = {
            "model": "gpt-4-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"What can you see on the picture?\n\n{prompt}"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 64
        }
        response = requests.post("https://api.openai.com/v1/chat/completions",
                                 headers={"Authorization": f"Bearer {self.open_ai_token}"},
                                 json=content)

        print(f"[OpenAIApi] Get the response: \"{response.json()}\"")
        return response.json()['choices'][0]['message']['content']

    def transcription(self, content):
        file_path = "to_transcript.mp3"
        if re.search(pattern='^http.://.*', string=content):
            sound_raw = requests.request("GET", content)
            with open(file_path, "wb") as f:
                f.write(sound_raw.content)
        elif re.search(pattern='^([a-zA-Z]):\\\\.*', string=content):
            if not os.path.isfile(content):
                print(f"[ERROR][OpenAIApi] A transcription of a file that does not exists was requested '{content}'")
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
