import os

# まず system 側の登録をリセット
c.ServerProxy.servers = {}

# named ルート "kafka_chatbot" を定義（★動的ポート）
c.ServerProxy.servers.update({
    "kafka_chatbot": {
        "command": [
            "/opt/conda/bin/python",
            "/home/jovyan/lab/openaiapi/src/kafka_chatbot_proxy.py",
            "--port", "8502"         # ★ jupyter-server-proxy が空きポートに置換
        ],
        # "port": は書かない（★動的に割り当てる）
        "cwd": "/home/jovyan/lab/openaiapi",
        "timeout": 60,
        "absolute_url": True,
        "launcher_entry": {"title": "Kafka Chatbot"},
        "environment": {
            "GRADIO_ROOT_PATH": "/proxy/8502",   # ★ Launcher URL と一致
            "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
            "PYTHONUNBUFFERED": "1",
            "OMP_NUM_THREADS": os.environ.get("OMP_NUM_THREADS", "2"),
            "OPENBLAS_NUM_THREADS": os.environ.get("OPENBLAS_NUM_THREADS", "2"),
            "MKL_NUM_THREADS": os.environ.get("MKL_NUM_THREADS", "2"),
            "NUMEXPR_NUM_THREADS": os.environ.get("NUMEXPR_NUM_THREADS", "2"),
        }
    }
})

# 念のため拡張の有効化も明示
c.ServerApp.jpserver_extensions = {"jupyter_server_proxy": True}
