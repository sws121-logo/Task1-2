import requests
from PyPDF2 import PdfReader
from models import processed_content
import uuid
import re
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')


async def process_url(url: str) -> str:
    response = requests.get(url)
    content = response.text
    cleaned_content = clean_text(content)
    chat_id = str(uuid.uuid4())
    processed_content[chat_id] = cleaned_content
    return chat_id


async def process_pdf(file) -> str:
    reader = PdfReader(file.file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    cleaned_content = clean_text(text)
    chat_id = str(uuid.uuid4())
    processed_content[chat_id] = cleaned_content
    return chat_id


def clean_text(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


async def chat_with_content(chat_id: str, question: str) -> str:
    if chat_id not in processed_content:
        raise ValueError("Chat ID not found.")

    content = processed_content[chat_id]
    content_embedding = model.encode(content)
    question_embedding = model.encode(question)

    # Calculate cosine similarity
    similarity = cosine_similarity([question_embedding], [content_embedding])

    # For simplicity, return the stored content for now
    return content
