from story_generator import StoryGenerator


def test_story_text():
    text_generator = StoryGenerator()
    category = input("Choose a catogory for the story: ")
    user_prompt = input("Write a description of the story: ")
    moral_prompt = input("Enter a moral: ")
    story_text_paragraphs = text_generator.generate_story_text(user_prompt, category, length=450, moral=moral_prompt)
    return story_text_paragraphs

if __name__ == "__main__":
    story_text_paragraphs = test_story_text()
    for paragraph in story_text_paragraphs:
        print(f"{paragraph} \n")