from fastmcp import FastMCP
import faiss, pickle, numpy as np
from openai import OpenAI
import os
import dotenv

dotenv.load_dotenv()

mcp = FastMCP(name="Kafka Brief an den Vater")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

dir_path = os.path.dirname(os.path.abspath(__file__))
index_path = os.path.join(dir_path, "kafka_brief.index")
metadata_path = os.path.join(dir_path, "kafka_metadata.pkl")
index = faiss.read_index(index_path)
with open(metadata_path, "rb") as f:
    metadatas = pickle.load(f)


@mcp.tool
def search(query: str, k: int = 3):
    emb = client.embeddings.create(input=[query], model="text-embedding-ada-002").data[0].embedding
    D, I = index.search(np.array([emb], dtype=np.float32), k)
    return [{"tag": metadatas[i]["tag"], "text": metadatas[i]["text"], "score": float(D[0][j])} for j, i in enumerate(I[0])]

# フェッチツール：任意idでチャンク返却
@mcp.tool
def fetch(tag: str):
    for md in metadatas:
        if md["tag"] == tag:
            return md
    raise ValueError(f"Unknown tag: {tag}")

if __name__ == "__main__":
    mcp.run(transport="stdio")
