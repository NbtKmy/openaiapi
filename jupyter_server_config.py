# Configuration file for jupyter-notebook.

c.ServerProxy.servers = {
    "kafka_chatbot": {
        "command": [
            "python",
            "/home/jovyan/lab/openaiapi/src/kafka_chatbot.py",
            "--port", "8502"
        ],
        "timeout": 60,
        "launcher_entry": {"title": "Kafka Chatbot"}
    }
}
