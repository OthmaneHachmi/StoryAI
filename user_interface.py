#Create the user interface using flask
from flask import Flask, render_template, request, send_file
from story_generator import StoryGenerator
from image_generator import ImageGenerator
from audio_generator import AudioGenerator

#create a Flask application instance
app = Flask(__name__)

text_generator = StoryGenerator()
image_generator = ImageGenerator()
audio_generator = AudioGenerator()

@app.route('/')
def index():
    return render_template('index.html')

# Create a route for generating the story with images
@app.route('/generate', methods=['GET', 'POST'])
def generate_story():
    prompt = request.form['prompt']
    category = request.form['category']
    length = int(request.form['length'])
    moral = request.form['moral']

    #Return the story text in a list of paragraphs
    paragraphs = text_generator.generate_story_text(prompt, category, length, moral)

    image_prompts = []
    image_urls = []
    for paragraph in paragraphs:
        image_prompt = image_generator.generate_image_prompt(paragraph)
        image_url = image_generator.generate_image(image_prompt)
        image_prompts.append(image_prompt)
        image_urls.append(image_url)



    #Return a list of urls of the generated images
    #images = [image_generator.generate_image(paragraph) for paragraph in paragraphs]
    #Pair the Paragraph and the images in a list :
    text_images = list(zip(paragraphs, image_urls))
    
    return render_template('index.html', text_images=text_images, story=' '.join(paragraphs))

# Create a route for generating the audio of the story
@app.route('/generate_audio', methods=['GET', 'POST'])
def generate_audio():
    story = request.form['story']
    voice = request.form['voice']
    
    # Generate audio for the story
    audio_stream = audio_generator.generate_audio(story, voice)
    
    return send_file(audio_stream, mimetype="audio/mpeg")

# Create a route for generating text only
@app.route('/test_text', methods=['GET', 'POST'])
def test_text():
    if request.method == 'POST':
        prompt = request.form['prompt']
        category = request.form['category']
        length = int(request.form['length'])
        moral = request.form['moral']
        story = text_generator.generate_story_text(prompt, category, length, moral)
        return render_template('test_text.html', story=story)
    return render_template('test_text.html')

# Create a route for generating images only
@app.route('/test_image', methods=['GET', 'POST'])
def test_image():
    if request.method == 'POST':
        image_prompt = request.form['image_prompt']
        image_url = image_generator.generate_image(image_prompt)
        return render_template('test_image.html', image_url=image_url)
    return render_template('test_image.html')

# Create a route for generating audio only
@app.route('/test_audio', methods=['GET', 'POST'])
def test_audio():
    if request.method == 'POST':
        audio_prompt = request.form['audio_prompt']
        voice = request.form['voice']
        audio_stream = audio_generator.generate_audio(audio_prompt, voice)
        temp_audio_file = "generated_audio.mp3"
        with open(temp_audio_file, "wb") as f:
            f.write(audio_stream.read())
        return render_template('test_audio.html', audio_url=f"/download_audio/{temp_audio_file}")

    return render_template('test_audio.html')

# Route to download the generated audio file
@app.route('/download_audio/<filename>')
def download_audio(filename):
    return send_file(filename, as_attachment=True)
if __name__ == '__main__':
    app.run(debug=True)