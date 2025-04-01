import gradio as gr
import requests
import os
from PIL import Image
from io import BytesIO

# Fetch API key from the environment variable
API_KEY = ""  
if not API_KEY:
    raise ValueError("Hugging Face API Key is missing! Set it in 'Repository secrets'.")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def generate_image(prompt):
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
    
    if response.status_code == 200:
        # Convert bytes to an image
        image = Image.open(BytesIO(response.content))
        image_path = "generated_image.png"  # Save it locally
        image.save(image_path)
        
        return image_path  # Return file path for Gradio
    else:
        return f"Error: {response.json()}"

# Gradio UI
iface = gr.Interface(
    fn=generate_image,
    inputs="text",
    outputs="image",  # Gradio will now correctly handle the image file path
    title="Text-to-Image Generator",
    description="Enter a text prompt and generate an AI image."
)

iface.launch()
