from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
from skimage.metrics import structural_similarity as ssim
import cv2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    real_file = request.files.get('real')
    fake_file = request.files.get('fake')

    if not real_file or not fake_file:
        return jsonify({'error': 'Both images are required'}), 400

    if not (allowed_file(real_file.filename) and allowed_file(fake_file.filename)):
        return jsonify({'error': 'Only png, jpg, jpeg, bmp formats are allowed'}), 400

    real_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(real_file.filename))
    fake_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(fake_file.filename))

    real_file.save(real_path)
    fake_file.save(fake_path)

    real_img = cv2.imread(real_path)
    fake_img = cv2.imread(fake_path)

    fake_img = cv2.resize(fake_img, (real_img.shape[1], real_img.shape[0]))

    real_gray = cv2.cvtColor(real_img, cv2.COLOR_BGR2GRAY)
    fake_gray = cv2.cvtColor(fake_img, cv2.COLOR_BGR2GRAY)

    score, _ = ssim(real_gray, fake_gray, full=True)

    result = 'NOT SAME' if score < 0.9 else 'SAME'

    return jsonify({'result': result, 'ssim_score': round(score, 4)})

if __name__ == '__main__':
    app.run(debug=True)
