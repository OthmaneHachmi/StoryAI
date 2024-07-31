#Create the user interface using flask
from flask import Flask, render_template, request
from story_generator import StoryGenerator
from image_generator import ImageGenerator

#create a Flask application instance
app = Flask(__name__)

text_generator = StoryGenerator()
image_generator = ImageGenerator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
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
    text_images = zip(paragraphs, images)
    
    return render_template('index.html', text_images=text_images)

if __name__ == '__main__':
    app.run(debug=True)