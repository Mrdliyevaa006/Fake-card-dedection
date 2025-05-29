from flask import Flask, request, jsonify
import numpy as np
import cv2
from skimage.metrics import structural_similarity as ssim
from PIL import Image

app = Flask(__name__)

def calculate_ssim(img1, img2):
    grayA = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    (score, diff) = ssim(grayA, grayB, full=True)
    return score

def prepare_image(file_storage):
    img = Image.open(file_storage).convert('RGB')
    img_np = np.array(img)
    img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    return img_cv

@app.route('/')
def index():
    return 'Fake Card Detection API is running!'

@app.route('/detect', methods=['POST'])
def detect():
    if 'real' not in request.files or 'fake' not in request.files:
        return jsonify({'error': 'Both real and fake images must be uploaded.'}), 400

    real_file = request.files['real']
    fake_file = request.files['fake']

    real_img = prepare_image(real_file)
    fake_img = prepare_image(fake_file)

    h_real, w_real = real_img.shape[:2]
    h_fake, w_fake = fake_img.shape[:2]

    new_w = min(w_real, w_fake)
    new_h = min(h_real, h_fake)

    real_resized = cv2.resize(real_img, (new_w, new_h))
    fake_resized = cv2.resize(fake_img, (new_w, new_h))

    score = calculate_ssim(real_resized, fake_resized)

    result = 'Fake' if score < 0.9 else 'Real'
    return jsonify({'ssim_score': score, 'result': result})

if __name__ == '__main__':
    app.run(debug=True)
