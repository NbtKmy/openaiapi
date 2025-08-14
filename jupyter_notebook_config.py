# Configuration file for jupyter-notebook.

c.ServerProxy.servers = {
    'chat_with_agent': {
        'command': [
            'python',
            './src/chat_with_agent.py',
            '--server.port', '8501',
            '--browser.serverAddress', '127.0.0.1:8501',
        ],
        'port': 8501,
        'timeout': 60
    },
    'kafka_chatbot': {
        'command': [
            'python',
            './src/kafka_chatbot.py',
            '--server.port', '8502',
            '--browser.serverAddress', '127.0.0.1:8502',
        ],
        'port': 8502,
        'timeout': 60
    }
}
