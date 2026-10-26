#!/bin/bash
# Exit script on first error
set -e

echo "[*] Step 1: Configuring local paths and variables..."
export WORKSPACE_DIR="/workspace"
export HF_HOME="${WORKSPACE_DIR}/hf_cache"
mkdir -p "$HF_HOME"

cd "$WORKSPACE_DIR"

echo "[*] Step 2: Ensuring uv package utility is installed..."
if ! command -v uv &> /dev/null; then
    curl -fsSL https://astral.sh | sh
    source $HOME/.local/bin/env
fi

echo "[*] Step 3: Spinning up local vLLM server with Qwen-VL..."
# uvx executes vllm in an isolated tool sandbox instantly
# Using nohup to let the server process run independently in the background
nohup uvx --with vllm vllm serve Qwen/Qwen2.5-VL-7B-Instruct \
    --port 8000 \
    --host 127.0.0.1 \
    --max-model-len 4096 \
    --limit-mm-per-prompt image=1 > vllm.log 2>&1 &

echo "[*] Step 4: Fetching Stable Diffusion WebUI environment..."
if [ ! -d "stable-diffusion-webui-forge" ]; then
    git clone https://github.com/lllyasviel/stable-diffusion-webui-forge.git
fi

cd stable-diffusion-webui-forge
echo "[*] Step 5: Booting Forge WebUI Engine..."
# Launches Forge with API endpoints enabled locally without starting a browser window
nohup python launch.py --api --listen --port 7860 --xformers --skip-torch-cuda-test > forge.log 2>&1 &

echo "[+] Infrastructure setup initiated successfully!"
echo "    - Monitor Qwen-VL startup: tail -f ${WORKSPACE_DIR}/vllm.log"
echo "    - Monitor Forge SD WebUI startup: tail -f ${WORKSPACE_DIR}/stable-diffusion-webui-forge/forge.log"

