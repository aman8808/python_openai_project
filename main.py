from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel
from db_functions import create_query, create_response, get_vectors
from config import OPENAI_API_KEY

app = FastAPI()

openai.api_key = OPENAI_API_KEY

tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")


class CustomHuggingFaceEmbeddings:
    def __init__(self, model_name):
        self.model_name = model_name

    async def embed(self, text):
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
        vector = outputs.last_hidden_state.mean(dim=1).numpy().flatten()
        if len(vector) > 300:
            return vector[:300]
        elif len(vector) < 300:
            return np.pad(vector, (0, 300 - len(vector)), 'constant')
        return vector


def create_index():
    vectors_data = get_vectors()
    vectors = np.array([vector_data[1] for vector_data in vectors_data], dtype=np.float32)
    return vectors, vectors_data


def find_nearest_neighbor(query_vector, vectors):
    distances = np.linalg.norm(vectors - query_vector, axis=1)
    nearest_idx = np.argmin(distances)
    return nearest_idx, distances[nearest_idx]

vectors, vectors_data = create_index()


class QueryData(BaseModel):
    query: str


@app.post("/generate-response/")
async def generate_response(query_data: QueryData):
    query_id = create_query(query_data.query)

    query_vector = text_to_vector(query_data.query)
    best_match_idx, best_similarity = find_nearest_neighbor(query_vector, vectors)

    similarity_threshold = 0.02
    if best_similarity < similarity_threshold:
        context = "Нет релевантной информации в базе данных."
    else:
        context = f"Контекст из базы данных: {vectors_data[best_match_idx][0]}"

    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system",
                 "content": "Ищи только информацию в моей базе данных по совпадению, не используй другие источники информации. Всегда отвечай на русском языке."},
                {"role": "user", "content": query_data.query},
                {"role": "assistant", "content": context}
            ],
            max_tokens=500
        )
        response_text = response.choices[0].message['content'].strip()
        tokens_used = response.usage['total_tokens']
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ошибка при запросе к OpenAI API")

    create_response(query_id, response_text, tokens_used)
    return {"query_id": query_id, "response": response_text}


def text_to_vector(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    vector = outputs.last_hidden_state.mean(dim=1).numpy().flatten()
    if len(vector) > 300:
        return vector[:300]
    elif len(vector) < 300:
        return np.pad(vector, (0, 300 - len(vector)), 'constant')
    return vector


@app.post("/vectors/")
async def add_vector(vector_data: dict):
    # Логика добавления вектора в базу данных
    return {"id": 1}


@app.get("/vectors/")
async def list_vectors():
    return {"vectors": []}
