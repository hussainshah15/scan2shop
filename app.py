from flask import Flask, request, jsonify, render_template
import numpy as np
from tensorflow.keras.applications.resnet import ResNet50, preprocess_input
from tensorflow.keras.preprocessing import image
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import requests
from io import BytesIO

app = Flask(__name__)
model = ResNet50(weights='imagenet', include_top=False, pooling='avg')

def calculate_similarity(feature_vector1, feature_vector2):
    similarity = cosine_similarity(feature_vector1.reshape(1, -1), feature_vector2.reshape(1, -1))
    return similarity[0][0]

def extract_features(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img = img.resize((224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features = model.predict(x)
    return features.flatten()

@app.route('/', methods=['GET'])
def index():
    # Return a message indicating that the app is running
    return "Flask app is running!")

@app.route('/similar-images', methods=['POST'])
def find_similar_images():
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid JSON data'})

    array1_images = data.get('array1_images')
    array2_images = data.get('array2_images')

    array1_features = []
    for img_url in array1_images:
        features = extract_features(img_url)
        array1_features.append(features)

    array2_features = []
    for img_url in array2_images:
        features = extract_features(img_url)
        array2_features.append(features)

    similar_images = []
    threshold = 0.4  # Adjust this value to set the similarity threshold
    for i, features1 in enumerate(array1_features):
        for j, features2 in enumerate(array2_features):
            similarity = calculate_similarity(features1, features2)
            if similarity >= threshold:
                similar_images.append((array2_images[j]))

    response = {
        'similarImages': similar_images
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run()
