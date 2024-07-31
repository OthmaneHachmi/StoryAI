from openai import OpenAI
import os
from dotenv import load_dotenv

class ImageGenerator:
    def __init__(self):
        #Load the evironment variables from .env file
        load_dotenv()
        
        #Get the api key from environment variables
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        #Define the model
        self.model = "dall-e-3"

    #Create the images generation function
    def generate_image(self, prompt):
        response = self.client.images.generate(
            model=self.model,
            prompt=prompt,
            size="1024x1024",
            quality="standard"
        )
        image_url = response.data[0].url
        return image_url
