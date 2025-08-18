import os

# Configuration file for jupyter-notebook.

c.ServerProxy.servers = {
    "kafka_chatbot": {
        #"command": [
        #    "python",
        #    "/home/jovyan/lab/openaiapi/src/kafka_chatbot_proxy.py",
        #    "--port", "8502"
        #],
        "command": [
            "bash","-lc",
            "exec /opt/conda/bin/python /home/jovyan/lab/openaiapi/src/kafka_chatbot_proxy.py --port 8502 2>&1 | tee /home/jovyan/gradio_8502.log"
        ],
        "port": 8502,
        "cwd": "/home/jovyan/lab/openaiapi",
        "timeout": 60,
        "launcher_entry": {"title": "Kafka Chatbot"},
        "environment": {
            "GRADIO_ROOT_PATH": "/kafka_chatbot",
            "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", "")
        }
    }
}
