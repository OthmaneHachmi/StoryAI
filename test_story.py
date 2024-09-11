from story_generator import StoryGenerator
from image_generator import ImageGenerator
from audio_generator import AudioGenerator

def test_story_text():
    text_generator = StoryGenerator()
    category = input("Choose a catogory for the story: ")
    user_prompt = input("Write a description of the story: ")
    moral_prompt = input("Enter a moral: ")
    paragraphs = text_generator.generate_story_text(user_prompt, category, length=450, moral=moral_prompt)
    print(paragraphs)

def test_story_image():
    image_generator = ImageGenerator()
    prompt = input("Enter a description for the image")
    image_url = image_generator.generate_image(prompt)
    print(image_url)


def test_image_prompt():
    text_generator = StoryGenerator()
    image_generator = ImageGenerator()
    category = input("Choose a catogory for the story: ")
    user_prompt = input("Write a description of the story: ")
    moral_prompt = input("Enter a moral: ")
    print("Generating ...")
    paragraphs = text_generator.generate_story_text(user_prompt, category, length=600, moral=moral_prompt)
    image_prompts = image_generator.generate_image_prompt(paragraphs)
    #image_prompts = []
    #for paragraph in paragraphs:
    #    image_prompt = image_generator.generate_image_prompt(paragraph)
    #    image_prompts.append(image_prompt)
    print(f"Generated Story: \n {paragraphs} \n")
    print(f"The image prompts: \n {image_prompts}")

#Uncomment the function you want to test
#test_story_image()
#test_story_text()
test_image_prompt()