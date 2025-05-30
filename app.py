from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
from skimage.metrics import structural_similarity as ssim
import cv2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}

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
        return jsonify({'error': 'Allowed image formats are png, jpg, jpeg, bmp'}), 400

    real_filename = secure_filename(real_file.filename)
    fake_filename = secure_filename(fake_file.filename)

    real_path = os.path.join(app.config['UPLOAD_FOLDER'], real_filename)
    fake_path = os.path.join(app.config['UPLOAD_FOLDER'], fake_filename)

    real_file.save(real_path)
    fake_file.save(fake_path)

    real_img = cv2.imread(real_path)
    fake_img = cv2.imread(fake_path)

    if real_img is None or fake_img is None:
        return jsonify({'error': 'Failed to read one or both images'}), 500

    fake_img = cv2.resize(fake_img, (real_img.shape[1], real_img.shape[0]))

    real_gray = cv2.cvtColor(real_img, cv2.COLOR_BGR2GRAY)
    fake_gray = cv2.cvtColor(fake_img, cv2.COLOR_BGR2GRAY)

    score, _ = ssim(real_gray, fake_gray, full=True)

    result = 'FAKE' if score < 0.9 else 'REAL'

    return jsonify({'result': result, 'ssim_score': score})

if __name__ == '__main__':
    app.run(debug=True)
