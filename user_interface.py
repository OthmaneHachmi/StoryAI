#Create the user interface using flask
from flask import Flask, render_template, request
from story_generator import StoryGenerator

#create a Flask application instance
app = Flask(__name__)

text_generator = StoryGenerator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_story():
    prompt = request.form['prompt']
    story = text_generator.generate_story_text(prompt)
    print(f"Generated story: {story}")
    return render_template('index.html', story=story)

if __name__ == '__main__':
    app.run(debug=True)