import os, json, asyncio, gradio as gr
from openai import OpenAI
from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport

# ---- 必須ENVの早期チェック ----
assert os.getenv("OPENAI_API_KEY"), "Missing OPENAI_API_KEY"

# OpenAI クライアント
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# パスの絶対化（Renkuでの確実性重視）
MCP_SCRIPT = "/home/jovyan/lab/openaiapi/src/kafka_brief_an_den_vater.py"
MCP_CWD    = "/home/jovyan/lab/openaiapi"

def generate_answer(query, contexts):
    context_text = "\n\n".join([f"[{c['tag']}] {c['text']}" for c in contexts])
    prompt = f"""Beantworte folgende Frage basierend auf dem untenstehenden Kontext.

Frage: {query}

Kontext:
{context_text}

Antwort:
"""
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Du bist ein Experte für Franz Kafka und seine Briefe."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=500,
    )
    return resp.choices[0].message.content.strip()

def format_sources_html(contexts):
    parts = []
    for c in contexts:
        tag = c["tag"]; score = c.get("score", 0.0)
        text = c["text"].replace("\n", "<br>")
        parts.append(
            f"<details><summary><strong>Seite: {tag}</strong> (score: {score:.3f})</summary>"
            f"<div style='margin-left:1em; font-size:0.95em;'>{text}</div></details>"
        )
    return "<h4>Quellen:</h4>" + "\n".join(parts)

async def run_mcp_rag(query, history):
    try:
        transport = PythonStdioTransport(
            script_path=MCP_SCRIPT,
            cwd=MCP_CWD,
            env={
                "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY",""),
                "PYTHONUNBUFFERED": "1",
            },
            startup_timeout=60.0,   # 起動が重い場合の保険
        )
        async with Client(transport) as client:
            result = await client.call_tool("search", {"query": query, "k": 3})
            contexts = json.loads(result.content[0].text)

        loop = asyncio.get_event_loop()
        answer = await loop.run_in_executor(None, generate_answer, query, contexts)
        return f"{answer}\n\n{format_sources_html(contexts)}"

    except Exception as e:
        return f"❌ エラー: {e}\n\n```\n{traceback.format_exc()}\n```"
    
iface = gr.ChatInterface(
    fn=run_mcp_rag,
    title="Kafka Brief an Vater MCP Chat (proxy)",
    chatbot=gr.Chatbot(label="KafkaBot", type="messages"),
    type="messages",
    textbox=gr.Textbox(placeholder="Frag hier alles zu Brief an Vater", label="Query"),
    examples=[
        "Wie war die Beziehung zwischen Kafka und seinem Vater?",
        "Was dachte Kafka über seine Schwestern?",
        "Welche Rolle spielte die Mutter?",
    ],
)

if __name__ == "__main__":
    root_path = os.getenv("GRADIO_ROOT_PATH", "/proxy/8502")  # Renku運用をデフォに
    iface.launch(
        server_port=8502,
        server_name="0.0.0.0",
        root_path=root_path,
        debug=True,
        show_error=True,
    )
