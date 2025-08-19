import os


c.ServerProxy.servers = {}


c.ServerProxy.servers.update({
    "kafka_chatbot_for_renku": {
        "command": [
            "/opt/conda/bin/python",
            "/home/jovyan/lab/openaiapi/src/kafka_chatbot_proxy.py",
            "--port", "8502"
        ],
        "cwd": "/home/jovyan/lab/openaiapi",
        "timeout": 60,
        "absolute_url": True,
        "path_info": "/proxy/8502",
        "launcher_entry": {"title": "Kafka Chatbot for Renku"},
        "environment": {
            "GRADIO_ROOT_PATH": "/proxy/8502",
            "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
            "PYTHONUNBUFFERED": "1",
        }
    }
})

# 念のため拡張の有効化も明示
c.ServerApp.jpserver_extensions = {"jupyter_server_proxy": True}
