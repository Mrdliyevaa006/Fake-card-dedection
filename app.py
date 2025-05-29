from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

app = Flask(__name__)

def calculate_ssim(img1, img2):
    grayA = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    (score, diff) = ssim(grayA, grayB, full=True)
    return score

@app.route('/')
def index():
    return render_template('index.html')  

@app.route('/detect', methods=['POST'])
def detect():
    if 'real' not in request.files or 'fake' not in request.files:
        return jsonify({'error': 'Both real and fake images must be uploaded.'}), 400

    real_file = request.files['real']
    fake_file = request.files['fake']

    real_np = np.frombuffer(real_file.read(), np.uint8)
    fake_np = np.frombuffer(fake_file.read(), np.uint8)

    real_img = cv2.imdecode(real_np, cv2.IMREAD_COLOR)
    fake_img = cv2.imdecode(fake_np, cv2.IMREAD_COLOR)

    real_img = cv2.resize(real_img, (fake_img.shape[1], fake_img.shape[0]))
    score = calculate_ssim(real_img, fake_img)

    result = 'Fake' if score < 0.9 else 'Real'
    return jsonify({'ssim_score': score, 'result': result})

if __name__ == '__main__':
    app.run(debug=True)
