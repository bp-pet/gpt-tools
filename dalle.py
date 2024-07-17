from openai import OpenAI

# load gpt key
import os
from dotenv import load_dotenv
load_dotenv()
key = os.getenv('GPT_TOKEN')

client = OpenAI(api_key=key)

prompt = "funny frog"

response = client.images.generate(
  model="dall-e-2",
  prompt=prompt,
  size="256x256",
  quality="standard",
  n=1,
)

image_url = response.data[0].url

print(image_url)                 