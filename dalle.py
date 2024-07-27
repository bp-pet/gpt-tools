from openai import OpenAI

# load gpt key
import os
from dotenv import load_dotenv
load_dotenv()
key = os.getenv('GPT_TOKEN')

client = OpenAI(api_key=key)

prompt = 'Test'

response = client.images.generate(
  model="dall-e-3",
  prompt=prompt,
  size="1024x1024",
  quality="standard",
  n=1,
)

for i in response.data:
  print(i.url)