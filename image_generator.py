from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

PLACEHOLDER_IMAGE = "https://placehold.co/1024x1024/e8d5b7/8b6914?text=Image+unavailable"

class ImageGenerator:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def generate_image(self, prompt):
        """Generate a single image from a prompt. Returns URL or placeholder on failure."""
        try:
            response = self.client.images.generate(
                model="dall-e-2",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            return response.data[0].url
        except Exception as e:
            print(f"[ImageGenerator] Image generation failed for prompt: {prompt[:60]}... Error: {e}")
            return PLACEHOLDER_IMAGE

    def generate_image_prompts(self, story_text):
        """
        Generate one image prompt per paragraph using GPT.
        Returns a list of prompt strings (one per paragraph).
        Falls back gracefully if parsing fails.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert image prompt generator for children's story illustrations.\n"
                            "A story will be given to you split into paragraphs.\n"
                            "For each paragraph, generate a short image prompt (under 70 words) "
                            "describing the scene in a child-friendly cartoon style.\n\n"
                            "Rules:\n"
                            "1. Always start every prompt with: 'A colored cartoon type sketch of,'\n"
                            "2. Keep prompts under 70 words.\n"
                            "3. Describe the scene simply — characters, setting, action.\n"
                            "4. No special characters except commas, hyphens, and periods.\n"
                            "5. Separate character traits and scene details with commas.\n\n"
                            "Return ONLY a valid JSON array of strings, one string per paragraph. "
                            "No explanation, no markdown, no backticks. Example:\n"
                            '["A colored cartoon type sketch of, ...", "A colored cartoon type sketch of, ..."]'
                        )
                    },
                    {"role": "user", "content": story_text}
                ],
                max_tokens=1500,
            )

            raw = response.choices[0].message.content.strip()

            # Strip markdown code fences if present
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
                raw = raw.strip()

            prompts = json.loads(raw)

            if isinstance(prompts, list) and all(isinstance(p, str) for p in prompts):
                return prompts

            raise ValueError("Unexpected JSON structure")

        except Exception as e:
            print(f"[ImageGenerator] Prompt generation failed: {e}")
            # Fallback: one generic prompt per paragraph
            paragraphs = [p.strip() for p in story_text.split("\n\n") if p.strip()]
            return [
                "A colored cartoon type sketch of, a colorful children's story scene, bright colors, friendly characters, cheerful setting."
                for _ in paragraphs
            ]

    def generate_images_parallel(self, prompts):
        """
        Generate multiple images in parallel using a thread pool.
        Returns a list of image URLs in the same order as the input prompts.
        """
        results = [PLACEHOLDER_IMAGE] * len(prompts)

        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_index = {
                executor.submit(self.generate_image, prompt): i
                for i, prompt in enumerate(prompts)
            }
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    results[index] = future.result()
                except Exception as e:
                    print(f"[ImageGenerator] Parallel image {index} failed: {e}")
                    results[index] = PLACEHOLDER_IMAGE

        return results