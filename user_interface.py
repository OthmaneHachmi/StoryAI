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
    #Return a list of urls of the generated images
    images = [image_generator.generate_image(paragraph) for paragraph in paragraphs]
    #Pair the Paragraph and the images in a list :
    text_images = list(zip(paragraphs, images))
    
    return render_template('index.html', text_images=text_images, story=' '.join(paragraphs))

# Create a route for generating the audio of the story
@app.route('/generate_audio', methods=['GET', 'POST'])
def generate_audio():
    story = request.form['story']
    
    # Generate audio for the story
    audio_stream = audio_generator.generate_audio(story)
    
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
        audio_url = audio_generator.generate_audio(audio_prompt)
        return render_template('test_audio.html', audio_url=audio_url)
    return render_template('test_audio.html')

if __name__ == '__main__':
    app.run(debug=True)