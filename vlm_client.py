# vlm_client.py
import base64
import requests
from config import QWEN_VLM_URL

def encode_image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def generate_tags_from_artwork(image_path: str) -> str:
    base64_image = encode_image_to_base64(image_path)
    
    prompt = (
        "Analyze this artwork. Describe the scene using strictly photorealistic physical tags "
        "ideal for Stable Diffusion prompting. Focus on lighting, specific materials, fine textures, "
        "and accurate human anatomy. Strip away all 2D illustration, comic, or ink stroke terminology."
    )
    
    payload = {
        "model": "Qwen/Qwen2.5-VL-7B-Instruct",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url", 
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                    }
                ]
            }
        ],
        "temperature": 0.2,
        "max_tokens": 200
    }
    
    try:
        response = requests.post(QWEN_VLM_URL, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()["choices"]["message"]["content"]
    except Exception as e:
        print(f"[!] Local vLLM connection error: {e}. Defaulting to generic tags.")
        return "raw photography, highly detailed, photorealistic skin texture"

