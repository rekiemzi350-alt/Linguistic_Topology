import torch
from diffusers import StableDiffusionPipeline
import sys
import os

def generate(prompt, output_file="generated_art.jpg"):
    model_id = "segmind/tiny-sd" # Small and fast for mobile/CPU
    
    print(f"Loading model {model_id}...")
    print("This will download approx 600MB on first run.")
    
    # Use CPU since Termux doesn't have CUDA/GPU access easily
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)
    pipe = pipe.to("cpu")
    
    # Reduce memory usage
    pipe.enable_attention_slicing()
    
    print(f"Generating image for prompt: '{prompt}'...")
    print("This may take 5-15 minutes on a phone CPU. Please wait...")
    
    # Generate
    # num_inference_steps=20 is a good balance for speed/quality on CPU
    image = pipe(prompt, num_inference_steps=20).images[0]
    
    # Save as JPG
    image.save(output_file, "JPEG", quality=95)
    print(f"Success! Image saved as {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_art.py 'your prompt here'")
    else:
        user_prompt = sys.argv[1]
        generate(user_prompt)
