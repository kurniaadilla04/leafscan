from flask import Blueprint, request, jsonify

# Create a blueprint for the routes
main = Blueprint('main', __name__)

@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    # Save the file to the uploads directory
    file.save(f'app/static/uploads/{file.filename}')
    return jsonify({'message': 'File uploaded successfully'}), 201

@main.route('/files', methods=['GET'])
def list_files():
    import os
    files = os.listdir('app/static/uploads')
    return jsonify(files), 200

@main.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200