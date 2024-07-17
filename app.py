# import the OpenAI Python library for calling the OpenAI API
from openai import OpenAI
import os
from dotenv import load_dotenv

#Load the evironment variables from .env file
load_dotenv()

#Get the api key from environment variables
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

#Define the model
MODEL = "gpt-3.5-turbo"

#Create a function to generate the story text
def generate_story_text():
    response = client.chat.completions.create(
        model = MODEL,
        messages = [
        {"role": "system", "content": "you are a story generator, you genetates stories for kids under 10 years old."},
        {"role": "user", "content": "generate a random story"}
        ],
        max_tokens=300,
        temperature=0.8
        )
    return response.choices[0].message.content

#Testing
story = generate_story_text()
print(story)