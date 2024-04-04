from AiDevsApi import AiDevsApi
from OpenAIApi import OpenAIApi
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import requests
import uuid


def search():
    api_aidevs = AiDevsApi()
    api_openai = OpenAIApi()
    client = QdrantClient(url="http://localhost:6333")
    url = 'https://unknow.news/archiwum_aidevs.json'
    collection_name = "ai_devs_search"

    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        on_disk_payload=True
    )

    archive = requests.get(url)
    if archive.status_code != 200:
        print(f"Failed to get '{url}' JSON, code = {archive.status_code}")
        exit(11)

    archive = archive.json()
    metadata = [{'title': entry['title'], 'info': entry['info'], 'url': entry['url'], 'id': uuid.uuid4()} for entry in archive]
    titles = [entry['title'] for entry in metadata]

    vectors = api_openai.multiple_embeddings(contents=titles, model='text-embedding-ada-002')

    client.upsert(
        collection_name=collection_name,
        points=[
            PointStruct(
                id=idx,
                vector=vector,
                payload=metadata[idx]
            )
            for idx, vector in enumerate(vectors)
        ]
    )

    ai_task = api_aidevs.get_task(task_name="search")
    question = ai_task['question']
    vector = api_openai.embeddings(content=question, model='text-embedding-ada-002')

    hits = client.search(collection_name=collection_name,
                         query_vector=vector,
                         limit=1)
    print(f"Found: {hits}")

    answer = {'answer': hits[0].payload['url']}
    api_aidevs.respond(answer=answer)
