# webui_client.py
import base64
import requests
from config import WEBUI_API_URL, SD_CHECKPOINT, CONTROLNET_SETTINGS

def trigger_img2img(image_path: str, vlm_prompt: str, output_path: str):
    with open(image_path, "rb") as img_file:
        init_image_b64 = base64.b64encode(img_file.read()).decode("utf-8")

    # Construct the multi-unit ControlNet list
    cn_units = [
        {
            "input_image": init_image_b64,
            "model": CONTROLNET_SETTINGS["depth"]["model"],
            "module": CONTROLNET_SETTINGS["depth"]["module"],
            "weight": CONTROLNET_SETTINGS["depth"]["weight"],
        },
        {
            "input_image": init_image_b64,
            "model": CONTROLNET_SETTINGS["openpose"]["model"],
            "module": CONTROLNET_SETTINGS["openpose"]["module"],
            "weight": CONTROLNET_SETTINGS["openpose"]["weight"],
        },
        {
            "input_image": init_image_b64,
            "model": CONTROLNET_SETTINGS["lineart"]["model"],
            "module": CONTROLNET_SETTINGS["lineart"]["module"],
            "weight": CONTROLNET_SETTINGS["lineart"]["weight"],
            "ending_step": CONTROLNET_SETTINGS["lineart"]["ending_step"],
        }
    ]

    payload = {
        "init_images": [init_image_b64],
        "prompt": f"{vlm_prompt}, masterpiece, photorealistic, 8k resolution, highly detailed skin texture, film grain",
        "negative_prompt": "2D, illustration, drawing, sketch, anime, graphic, bad hands, deformed face, smooth plastic skin",
        "steps": 28,
        "cfg_scale": 5.5,
        "denoising_strength": 0.60,
        "override_settings": {
            "sd_model_checkpoint": SD_CHECKPOINT
        },
        "alwayson_scripts": {
            "ControlNet": {"args": cn_units},
            "ADetailer": {
                "args": [
                    True,  # Global execution switch
                    {
                        "ad_model": "face_yolov8s.pt",
                        "ad_prompt": "highly detailed realistic face, sharp focus photography portrait",
                        "ad_confidence": 0.3
                    },
                    {
                        "ad_model": "hand_yolov8n.pt",
                        "ad_prompt": "perfect hands, highly detailed realistic fingers",
                        "ad_confidence": 0.3
                    }
                ]
            }
        }
    }

    print("[*] Dispatching compilation payload to Forge/WebUI API...")
    response = requests.post(f"{WEBUI_API_URL}/sdapi/v1/img2img", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        image_data = base64.b64decode(result["images"][0])
        with open(output_path, "wb") as out_file:
            out_file.write(image_data)
        print(f"[+] Render complete! File stored -> {output_path}")
    else:
        print(f"[!] Engine Error ({response.status_code}): {response.text}")


