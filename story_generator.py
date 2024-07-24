# import the OpenAI Python library for calling the OpenAI API
from openai import OpenAI
import os
from dotenv import load_dotenv

class StoryGenerator:
    def __init__(self):
        #Load the evironment variables from .env file
        load_dotenv()
        
        #Get the api key from environment variables
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        #Define the model
        self.MODEL = "gpt-3.5-turbo"
    

    #Create a function to generate the story text
    def generate_story_text(self, prompt, category, length, moral):
        category_prompt = f"Category: {category}. "
        length_prompt = f"Length: {length}. "
        moral_prompt = f"Include this moral {moral}. " if moral else ""
        full_prompt = f"{category_prompt}{length_prompt}{prompt}. {moral_prompt}"
        
        response = self.client.chat.completions.create(
            model = self.MODEL,
            messages = [
            {"role": "system", "content": "you are a story generator, you genetate stories in a certain catrgory given in the prompt. These stories are for kids under 10 years old."},
            {"role": "user", "content": full_prompt}
            ],
            #Set the length of the story
            max_tokens=length,
        )
        story_text = response.choices[0].message.content

        #Split the story in paragraphs
        paragraphs = story_text.split('\n\n')
        return paragraphs