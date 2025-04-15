# app.py
from flask import Flask, render_template, request, jsonify
from image_retrieval import create_moodboard

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/moodboard', methods=['POST'])
def get_moodboard():
    data = request.json
    prompt = data.get('prompt', '')
    domain = data.get('domain')
    num_images = int(data.get('num_images', 16))
    
    images = create_moodboard(prompt, num_images, domain)
    return jsonify({'images': images})

if __name__ == '__main__':
    app.run(debug=True, port=5000)