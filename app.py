from flask import Flask, request, jsonify, send_from_directory
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import io

app = Flask(__name__)
model = load_model('model.h5')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/graph')
def graph():
    return send_from_directory('.', 'training_graphs.png')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['image']
    img = Image.open(io.BytesIO(file.read())).convert('RGB').resize((64, 64))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)[0][0]
    label = 'Cat' if prediction < 0.5 else 'Dog'
    confidence = float(1 - prediction) if prediction < 0.5 else float(prediction)

    return jsonify({ 'label': label, 'confidence': round(confidence * 100, 2) })

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
