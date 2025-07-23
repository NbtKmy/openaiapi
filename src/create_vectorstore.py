from bs4 import BeautifulSoup
import re
import os
from dotenv import load_dotenv
import pandas as pd
from openai import OpenAI
import faiss
import numpy as np
import pickle


load_dotenv()


file_path = "./data/Brief_an_den_Vater_Wikisource.html"

with open(file_path, "r", encoding="utf-8") as file:
    html = file.read()

soup = BeautifulSoup(html, "lxml")

text = soup.find_all("p")

all_text = ""
for para in text:
    all_text += para.get_text()

pattern = r"(\[\d+[a-z]\])"
parts = re.split(pattern, all_text)
chunks = []
for i in range(1, len(parts), 2):
    tag = parts[i]
    content = parts[i + 1].strip()
    chunks.append({"tag": tag, "text": content})

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(text):
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

embeddings = []
metadatas = []

for chunk in chunks:
    emb = get_embedding(chunk["text"])
    embeddings.append(emb)
    metadatas.append({"tag": chunk["tag"], "text": chunk["text"]})

dimension = len(embeddings[0])
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings).astype("float32"))

faiss.write_index(index, "kafka_brief.index")
with open("kafka_metadata.pkl", "wb") as f:
    pickle.dump(metadatas, f)
