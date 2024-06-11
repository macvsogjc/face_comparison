from flask import Flask, request, jsonify
import face_recognition
import os
from werkzeug.utils import secure_filename
import zipfile

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def save_image(file, folder):
    filename = secure_filename(file.filename)
    filepath = os.path.join(folder, filename)
    file.save(filepath)
    return filepath

@app.route('/compare', methods=['POST'])
def compare_faces():
    reference_image_file = request.files['referenceImage']
    zip_file = request.files['zipFile']

    # Save and process the reference image
    reference_image_path = save_image(reference_image_file, app.config['UPLOAD_FOLDER'])
    reference_image = face_recognition.load_image_file(reference_image_path)
    reference_encoding = face_recognition.face_encodings(reference_image)[0]

    # Extract and process the images from the zip file
    zip_path = save_image(zip_file, app.config['UPLOAD_FOLDER'])
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(app.config['UPLOAD_FOLDER'])

    results = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename == os.path.basename(reference_image_path) or filename.endswith('.zip'):
            continue
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            match = face_recognition.compare_faces([reference_encoding], encodings[0])
            results.append({
                'image': filename,
                'match': match[0]
            })
        else:
            results.append({
                'image': filename,
                'match': False,
                'error': 'No faces found'
            })

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
