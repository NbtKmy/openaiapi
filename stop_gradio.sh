#!/usr/bin/env bash
set -euo pipefail
pkill -f kafka_chatbot_proxy.py || true
pkill -f gradio || true
pkill -f uvicorn || true
echo "[STOP] done."
