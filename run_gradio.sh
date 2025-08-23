#!/usr/bin/env bash
set -euo pipefail

# ---- 設定 ----
PORT="${PORT:-8502}"

# Renku が注入するセッションのベースパスに /proxy/<port> をつなぐ
BASE_PATH="${RENKU_BASE_URL_PATH:-/sessions/unknown}"
ROOT_PATH="${BASE_PATH%/}/proxy/${PORT}"

# 並列抑制（任意）
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-2}"
export OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-2}"
export MKL_NUM_THREADS="${MKL_NUM_THREADS:-2}"
export NUMEXPR_NUM_THREADS="${NUMEXPR_NUM_THREADS:-2}"
export PYTHONUNBUFFERED=1

# 既存プロセス掃除
pkill -f kafka_chatbot_proxy.py || true
pkill -f gradio || true
pkill -f uvicorn || true

# 起動
LOG="${HOME}/gradio_${PORT}.log"
echo "[BOOT] starting Gradio port=${PORT} root_path=${ROOT_PATH}" | tee -a "$LOG"

nohup /opt/conda/bin/python /home/jovyan/lab/openaiapi/src/kafka_chatbot_proxy.py \
  --port "${PORT}" \
  --root_path "${ROOT_PATH}" \
  >> "${LOG}" 2>&1 &

echo "[BOOT] logs -> ${LOG}"
echo "[BOOT] open this in the browser:"
echo "       ${RENKU_BASE_URL:-https://renkulab.io}${ROOT_PATH}/"
