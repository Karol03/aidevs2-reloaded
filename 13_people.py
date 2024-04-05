from AiDevsApi import AiDevsApi
from OpenAIApi import OpenAIApi
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import requests
import uuid


def people():
    api_aidevs = AiDevsApi()
    api_openai = OpenAIApi(temperature=0)
    client = QdrantClient(url="http://localhost:6333")
    url = 'https://tasks.aidevs.pl/data/people.json'
    collection_name = "ai_devs_people"

    # Create collection to store data about people
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        on_disk_payload=True
    )

    # Get the JSON with people data and parse it into the list
    records = requests.get(url)
    if records.status_code != 200:
        print(f"Failed to get '{url}' JSON, code = {records.status_code}")
        exit(11)

    records = records.json()
    descriptions = [{'name': entry['imie'],
                     'surname': entry['nazwisko'],
                     'age': entry['wiek'],
                     'about': entry['o_mnie'],
                     'captain_bomba': entry['ulubiona_postac_z_kapitana_bomby'],
                     'series': entry['ulubiony_serial'],
                     'film': entry['ulubiony_film'],
                     'color': entry['ulubiony_kolor'],
                     'id': uuid.uuid4()}
                    for entry in records]
    full_names = [f"{entry['name']} {entry['surname']}" for entry in descriptions]

    # Get list of embeddings of full names
    vectors = api_openai.multiple_embeddings(contents=full_names, model='text-embedding-ada-002')

    # Using embeddings of the full names insert all records into the database
    client.upsert(
        collection_name=collection_name,
        points=[
            PointStruct(
                id=idx,
                vector=vector,
                payload=descriptions[idx]
            )
            for idx, vector in enumerate(vectors)
        ]
    )

    # Get the 'people' task and extract from it the name of the person about whom the question is about
    ai_task = api_aidevs.get_task(task_name="people")
    question = ai_task['question']

    system = """
Przykłady:```
U: Gdzie mieszka Julian Kwiatkowski?
A: Julian Kwiatkowski

U: Kto ostatni widział Jarosława Kalinowskiego?
A: Jarosław Kalinowski

U: Ile lat ma Olaf Mazurek?
A: Olaf Mazurek
```
"""

    full_name = api_openai.chat(prompt=question, system=system)

    # Convert this full name into embeddings and find person in the database
    vector = api_openai.embeddings(content=full_name, model='text-embedding-ada-002')
    hits = client.search(collection_name=collection_name,
                         query_vector=vector,
                         limit=1)

    # Using data about the person, we ask the chat to answer the question
    about_person = f"""
{full_name}
wiek: {hits[0].payload['age']}
o osobie: {hits[0].payload['about']}
ulubiona postać z kapitana bomby: {hits[0].payload['captain_bomba']}
ulubiony serial: {hits[0].payload['series']}
ulubiony film: {hits[0].payload['film']}
ulubiony kolor: {hits[0].payload['color']}
"""

    answer = api_openai.chat(prompt=question, system=about_person)
    answer = {'answer': answer}
    api_aidevs.respond(answer=answer)
