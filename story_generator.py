from openai import OpenAI
import os
from dotenv import load_dotenv

class StoryGenerator:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.MODEL = "gpt-3.5-turbo"

    def generate_story_text(self, prompt, category, length, moral):
        category_prompt = f"Category: {category}. "
        length_prompt = f"Length: approximately {length} tokens. "
        moral_prompt = f"Include this moral: {moral}. " if moral else ""
        full_prompt = f"{category_prompt}{length_prompt}{prompt}. {moral_prompt}"

        try:
            response = self.client.chat.completions.create(
                model=self.MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a story generator for children under 10 years old. "
                            "Write engaging, age-appropriate stories. "
                            "Separate each paragraph with a blank line (double newline). "
                            "Do not include a title, just the story. "
                            "Write between 5 and 9 paragraphs."
                        )
                    },
                    {"role": "user", "content": full_prompt}
                ],
                max_tokens=length,
            )
            story_text = response.choices[0].message.content.strip()
            return story_text

        except Exception as e:
            raise RuntimeError(f"Story generation failed: {str(e)}")