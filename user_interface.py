from flask import Flask, render_template, request, send_file, jsonify
from story_generator import StoryGenerator
from image_generator import ImageGenerator
from audio_generator import AudioGenerator

app = Flask(__name__)

text_generator = StoryGenerator()
image_generator = ImageGenerator()
audio_generator = AudioGenerator()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate_story():
    prompt   = request.form.get('prompt', '').strip()
    category = request.form.get('category', 'Random')
    length   = int(request.form.get('length', 500))
    moral    = request.form.get('moral', '').strip()

    error = None
    text_images = []
    story = ''

    try:
        # 1. Generate story text
        story_text = text_generator.generate_story_text(prompt, category, length, moral)

        # 2. Split into paragraphs
        paragraphs = [p.strip() for p in story_text.split('\n\n') if p.strip()]
        story = ' '.join(paragraphs)

        # 3. Generate image prompts (one per paragraph, via JSON)
        image_prompts = image_generator.generate_image_prompts(story_text)

        # Align lengths — pad or trim so they match paragraph count
        while len(image_prompts) < len(paragraphs):
            image_prompts.append(image_prompts[-1] if image_prompts else
                "A colored cartoon type sketch of, a colorful children's story scene.")
        image_prompts = image_prompts[:len(paragraphs)]

        # 4. Generate images in parallel
        image_urls = image_generator.generate_images_parallel(image_prompts)

        # 5. Zip paragraphs and images
        text_images = list(zip(paragraphs, image_urls))

    except Exception as e:
        error = str(e)
        print(f"[generate_story] Error: {e}")

    return render_template('index.html',
                           text_images=text_images,
                           story=story,
                           error=error)


@app.route('/generate_audio', methods=['POST'])
def generate_audio():
    story = request.form.get('story', '')
    voice = request.form.get('voice', 'pNInz6obpgDQGcFmaJgB')

    try:
        audio_stream = audio_generator.generate_audio(story, voice)
        return send_file(audio_stream, mimetype="audio/mpeg")
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/test_text', methods=['GET', 'POST'])
def test_text():
    story = None
    error = None
    if request.method == 'POST':
        try:
            prompt   = request.form.get('prompt', '')
            category = request.form.get('category', 'Random')
            length   = int(request.form.get('length', 450))
            moral    = request.form.get('moral', '')
            story    = text_generator.generate_story_text(prompt, category, length, moral)
        except Exception as e:
            error = str(e)
    return render_template('test_text.html', story=story, error=error)


@app.route('/test_image', methods=['GET', 'POST'])
def test_image():
    image_url = None
    error = None
    if request.method == 'POST':
        try:
            image_prompt = request.form.get('image_prompt', '')
            image_url    = image_generator.generate_image(image_prompt)
        except Exception as e:
            error = str(e)
    return render_template('test_image.html', image_url=image_url, error=error)


@app.route('/test_audio', methods=['GET', 'POST'])
def test_audio():
    audio_url = None
    error = None
    if request.method == 'POST':
        try:
            audio_prompt = request.form.get('audio_prompt', '')
            voice        = request.form.get('voice', 'pNInz6obpgDQGcFmaJgB')
            audio_stream = audio_generator.generate_audio(audio_prompt, voice)
            temp_file    = "generated_audio.mp3"
            with open(temp_file, "wb") as f:
                f.write(audio_stream.read())
            audio_url = f"/download_audio/{temp_file}"
        except Exception as e:
            error = str(e)
    return render_template('test_audio.html', audio_url=audio_url, error=error)


@app.route('/download_audio/<filename>')
def download_audio(filename):
    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)