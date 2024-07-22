from story_generator import StoryGenerator


def test():
    text_generator = StoryGenerator()
    category = input("Choose a catogory for the story")
    user_prompt = input("Write a description of the story")
    story_text = text_generator.generate_story_text(user_prompt, category, length=450)
    return story_text

if __name__ == "__main__":
    story_text = test()
    print(story_text)