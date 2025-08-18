import gradio as gr
import dotenv
import asyncio
from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport
import os
import json
from openai import OpenAI


dotenv.load_dotenv()
assert os.getenv("OPENAI_API_KEY"), "Missing OPENAI_API_KEY"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

script_path = os.path.join(os.path.dirname(__file__), "kafka_brief_an_den_vater.py")
transport = PythonStdioTransport(script_path=script_path)

def generate_answer(query, contexts):

    context_text = "\n\n".join([f"[{c['tag']}] {c['text']}" for c in contexts])

    prompt = f"""
Beantworte folgende Frage basierend auf dem untenstehenden Kontext.

Frage: {query}

Kontext:
{context_text}

Antwort:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Du bist ein Experte für Franz Kafka und seine Briefe."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=500
    )

    return response.choices[0].message.content.strip()

def format_sources_html(contexts):
    parts = []
    for c in contexts:
        tag = c["tag"]
        score = c.get("score", 0.0)
        text = c["text"].replace("\n", "<br>")  # 改行整形

        parts.append(f"""<details>
<summary><strong>Seite: {tag}</strong> (score: {score:.3f})</summary>
<div style="margin-left:1em; font-size: 0.95em;">{text}</div>
</details>""")

    return "<h4>Quellen:</h4>" + "\n".join(parts)

async def run_mcp_rag(query, history):
    async with Client(transport) as client:
        # Step 1: MCP rufen, um relevante Kontextinformationen zu erhalten
        result = await client.call_tool("search", {"query": query, "k": 3})
        contexts = json.loads(result.content[0].text)
        # Step 2: OpenAI API verwenden, um Antwort zu generieren
        loop = asyncio.get_event_loop()
        answer = await loop.run_in_executor(None, generate_answer, query, contexts)
        # Step 3: Antwort formatieren und Quellen angeben

        sources_html = format_sources_html(contexts)
        full_response = f"{answer}\n\n{sources_html}"
        #sources = "\n".join([f"Seite: {c['tag']} (score: {c['score']:.3f})" for c in contexts])
        return full_response


iface = gr.ChatInterface(
    fn=run_mcp_rag,
    title="Kafka Brief an Vater MCP Chat",
    chatbot=gr.Chatbot(label="KafkaBot", type="messages"),
    type="messages",
    textbox=gr.Textbox(placeholder="Frag hier alles zu Brief an Vater", label="Query"),
    examples=[
        "Wie war die Beziehung zwischen Kafka und seinem Vater?",
        "Was dachte Kafka über seine Schwestern?",
        "Welche Rolle spielte die Mutter?"
    ]
)

if __name__ == "__main__":


    root_path = os.getenv("GRADIO_ROOT_PATH", "")
    iface.launch(
        server_port=8502,
        server_name="0.0.0.0",
        root_path=root_path,
        debug=True, 
        show_error=True
        )
