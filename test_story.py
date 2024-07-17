from story_generator import StoryGenerator


def test():
    text_generator = StoryGenerator()
    user_prompt = input("Enter a prompt to generate a story")
    story_text = text_generator.generate_story_text(user_prompt)
    return story_text

if __name__ == "__main__":
    story_text = test()
    print(story_text)