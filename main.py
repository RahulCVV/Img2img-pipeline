
# main.py
import sys
import os
from vlm_client import generate_tags_from_artwork
from webui_client import trigger_img2img

def run_pipeline(input_image: str, output_image: str):
    if not os.path.exists(input_image):
        print(f"[!] Input image '{input_image}' not found.")
        return

    print(f"[*] Phase 1: Scanning '{input_image}' via local Qwen-VL inside vLLM...")
    vlm_prompt = generate_tags_from_artwork(input_image)
    print(f"[+] Physical tags generated successfully:\n> {vlm_prompt}\n")
    
    print("[*] Phase 2: Transmitting structure & prompt tokens to generation engine...")
    trigger_img2img(input_image, vlm_prompt, output_image)

if __name__ == "__main__":
    input_path = sys.argv[1] if len(sys.argv) > 1 else "input.png"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "output.png"
    
    run_pipeline(input_path, output_path)


