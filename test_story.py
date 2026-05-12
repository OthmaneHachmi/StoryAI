from story_generator import StoryGenerator
from image_generator import ImageGenerator
from audio_generator import AudioGenerator


def test_story_text():
    """Test story text generation only."""
    text_generator = StoryGenerator()
    category    = input("Category (e.g. Adventure, Fantasy, Animals stories): ").strip() or "Random"
    user_prompt = input("Story description (optional, press Enter to skip): ").strip()
    moral       = input("Moral lesson (optional, press Enter to skip): ").strip()
    length      = int(input("Length in tokens (450 / 900 / 1200): ").strip() or "450")

    print("\n⏳ Generating story...\n")
    story = text_generator.generate_story_text(user_prompt, category, length, moral)
    print("=" * 60)
    print(story)
    print("=" * 60)


def test_story_image():
    """Test single image generation from a manual prompt."""
    image_generator = ImageGenerator()
    prompt = input("Enter image prompt: ").strip()

    print("\n⏳ Generating image...\n")
    image_url = image_generator.generate_image(prompt)
    print(f"✅ Image URL:\n{image_url}")


def test_image_prompts():
    """Generate a story and print the AI-generated image prompts (no images)."""
    text_generator  = StoryGenerator()
    image_generator = ImageGenerator()

    category    = input("Category: ").strip() or "Random"
    user_prompt = input("Story description (optional): ").strip()
    moral       = input("Moral (optional): ").strip()
    length      = int(input("Length in tokens (450 / 900 / 1200): ").strip() or "600")

    print("\n⏳ Generating story and image prompts...\n")
    story   = text_generator.generate_story_text(user_prompt, category, length, moral)
    prompts = image_generator.generate_image_prompts(story)

    print("=" * 60)
    print("STORY:\n")
    print(story)
    print("\n" + "=" * 60)
    print(f"IMAGE PROMPTS ({len(prompts)} total):\n")
    for i, p in enumerate(prompts, 1):
        print(f"[{i}] {p}\n")
    print("=" * 60)


def test_full_pipeline():
    """Run the full pipeline: story → image prompts → images (parallel)."""
    text_generator  = StoryGenerator()
    image_generator = ImageGenerator()

    category    = input("Category: ").strip() or "Random"
    user_prompt = input("Story description (optional): ").strip()
    moral       = input("Moral (optional): ").strip()
    length      = int(input("Length in tokens (450 / 900 / 1200): ").strip() or "600")

    print("\n⏳ Generating story...\n")
    story      = text_generator.generate_story_text(user_prompt, category, length, moral)
    paragraphs = [p.strip() for p in story.split("\n\n") if p.strip()]

    print(f"📖 Story ({len(paragraphs)} paragraphs):\n")
    for i, p in enumerate(paragraphs, 1):
        print(f"[{i}] {p}\n")

    print("⏳ Generating image prompts...\n")
    prompts = image_generator.generate_image_prompts(story)

    # Align lengths
    while len(prompts) < len(paragraphs):
        prompts.append(prompts[-1])
    prompts = prompts[:len(paragraphs)]

    print(f"🎨 Generating {len(prompts)} images in parallel...\n")
    image_urls = image_generator.generate_images_parallel(prompts)

    print("=" * 60)
    print("RESULTS:\n")
    for i, (para, url) in enumerate(zip(paragraphs, image_urls), 1):
        print(f"[{i}] {para[:80]}{'...' if len(para) > 80 else ''}")
        print(f"    🖼  {url}\n")
    print("=" * 60)


def test_audio():
    """Test audio generation."""
    audio_generator = AudioGenerator()
    text  = input("Enter text to narrate: ").strip()
    voice = input("Voice ID (press Enter for default male voice): ").strip()
    voice = voice or "pNInz6obpgDQGcFmaJgB"

    print("\n⏳ Generating audio...\n")
    audio_stream = audio_generator.generate_audio(text, voice)
    out_file = "test_output.mp3"
    with open(out_file, "wb") as f:
        f.write(audio_stream.read())
    print(f"✅ Audio saved to: {out_file}")


# ── Menu ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    menu = {
        "1": ("Test story text only",          test_story_text),
        "2": ("Test single image generation",  test_story_image),
        "3": ("Test image prompt generation",  test_image_prompts),
        "4": ("Test full pipeline (story + images)", test_full_pipeline),
        "5": ("Test audio generation",         test_audio),
    }

    print("\n📖 StoryAI — Test Runner\n")
    for key, (label, _) in menu.items():
        print(f"  {key}. {label}")

    choice = input("\nChoose a test (1–5): ").strip()

    if choice in menu:
        print()
        try:
            menu[choice][1]()
        except Exception as e:
            print(f"\n❌ Error: {e}")
    else:
        print("Invalid choice.")