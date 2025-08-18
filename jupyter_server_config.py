import os

# Configuration file for jupyter-notebook.

c.ServerProxy.servers = {
    "kafka_chatbot": {
        "command": [
            "python",
            "/home/jovyan/lab/openaiapi/src/kafka_chatbot.py",
            "--port", "8502"
        ],
        "port": 8502,
        "cwd": "/home/jovyan/lab/openaiapi",
        "timeout": 60,
        "launcher_entry": {"title": "Kafka Chatbot"},
        "environment": {
            "GRADIO_ROOT_PATH": "/proxy/8502",
            "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", "")
        }
    }
}
