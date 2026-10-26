# Internal network mappings
WEBUI_API_URL = "http://127.0.0.1:7860"
QWEN_VLM_URL = "http://127.0.0"

# Stable Diffusion Setup
SD_CHECKPOINT = "realisticVisionV60_v60VAE.safetensors"

# ControlNet 1.1 Structural Weights
CONTROLNET_SETTINGS = {
    "depth": {
        "model": "control_v11f1p_sd15_depth",
        "module": "depth_zoe",
        "weight": 1.0
    },
    "openpose": {
        "model": "control_v11p_sd15_openpose",
        "module": "openpose_full",
        "weight": 1.0
    },
    "lineart": {
        "model": "control_v11p_sd15_lineart",
        "module": "lineart_realistic",
        "weight": 0.35,
        "ending_step": 0.4  # Early cutoff prevents 2D grids from baking into textures
    }
}
