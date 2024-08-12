from story_generator import StoryGenerator
from image_generator import ImageGenerator
from audio_generator import AudioGenerator

def test_story_text():
    text_generator = StoryGenerator()
    category = input("Choose a catogory for the story: ")
    user_prompt = input("Write a description of the story: ")
    moral_prompt = input("Enter a moral: ")
    story_text_paragraphs = text_generator.generate_story_text(user_prompt, category, length=450, moral=moral_prompt)
    print(story_text_paragraphs)

def test_story_image():
    image_generator = ImageGenerator()
    prompt = input("Enter a description for the image")
    image_url = image_generator.generate_image(prompt)
    print(image_url)

#Uncomment the function you want to test
#test_story_image()
#test_story_text()
