import os

service = "kafka_chatbot_for_renku"
base = os.environ.get("RENKU_BASE_URL_PATH", "")
root = (base.rstrip("/") + "/" + service) if base else ("/" + service)

c.ServerProxy.servers = {}


c.ServerProxy.servers.update({
    "kafka_chatbot_for_renku": {
        "command": [
            "/opt/conda/bin/python",
            "/home/jovyan/lab/openaiapi/src/kafka_chatbot_proxy.py",
            "--port", "8502",
            "--root_path", root,  
        ],
        "cwd": "/home/jovyan/lab/openaiapi",
        "timeout": 60,
        "launcher_entry": {"title": "Kafka Chatbot for Renku"},
        "environment": {
            "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
            "PYTHONUNBUFFERED": "1",
        }
    }
})

# 念のため拡張の有効化も明示
c.ServerApp.jpserver_extensions = {"jupyter_server_proxy": True}
