# 📖 StoryAI

A web app that generates illustrated children's stories with narration — powered by OpenAI and ElevenLabs.

Give it a prompt, pick a category and length, and StoryAI writes a story, illustrates each paragraph with AI-generated cartoon images, and reads it aloud in your chosen voice.

## Features

- **Story generation** — GPT-3.5-turbo writes age-appropriate stories (for children under 10) in categories like Fantasy, Adventure, Animals, Educational, Sci-fi, Mystery, and Comedy
- **AI illustration** — DALL-E 2 generates a cartoon image for each paragraph, prompted automatically by the story content
- **Text-to-speech narration** — ElevenLabs converts the full story to audio in a male or female voice, playable directly in the browser
- **Storybook layout** — alternating left/right image-and-text pages, warm storybook design
- **Customizable** — set a story description, category, length (short / medium / long), and optional moral lesson

### Prerequisites

- Python 3.9+
- An OpenAI API key
- An ElevenLabs API key

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/your-username/storyai.git
cd storyai
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv
source venv/bin/activate       # Linux
venv\Scripts\activate          # Windows
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

**5. Run the app**

```bash
python user_interface.py
```

Open your browser at `http://127.0.0.1:5000`


## CLI Test Runner

`test_story.py` lets you test each part of the pipeline from the terminal without running the web server:

```bash
python test_story.py
```

```
📖 StoryAI — Test Runner

  1. Test story text only
  2. Test single image generation
  3. Test image prompt generation
  4. Test full pipeline (story + images)
  5. Test audio generation

Choose a test (1–5):
```
