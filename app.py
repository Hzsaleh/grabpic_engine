from flask import Flask, request, jsonify
import face_recognition
import sqlite3
import pickle

app = Flask(__name__)

@app.route('/authenticate', methods=['POST'])
def authenticate():
    if 'file' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
        
    file = request.files['file']
    image = face_recognition.load_image_file(file)
    encodings = face_recognition.face_encodings(image)
    
    if not encodings:
        return jsonify({"error": "No face found in selfie"}), 400
        
    uploaded_encoding = encodings[0]
    
    conn = sqlite3.connect('grabpic.db')
    cursor = conn.cursor()
    cursor.execute("SELECT grab_id, face_encoding FROM Faces")
    faces = cursor.fetchall()
    conn.close()
    
    known_encodings = [pickle.loads(f[1]) for f in faces]
    known_ids = [f[0] for f in faces]
    
    if not known_encodings:
        return jsonify({"error": "Database empty"}), 404
        
    matches = face_recognition.compare_faces(known_encodings, uploaded_encoding, tolerance=0.5)
    
    if True in matches:
        matched_id = known_ids[matches.index(True)]
        return jsonify({"status": "success", "grab_id": matched_id})
        
    return jsonify({"error": "Face not recognized"}), 401
@app.route('/images/<int:grab_id>', methods=['GET'])
def get_images(grab_id):
    conn = sqlite3.connect('grabpic.db')
    cursor = conn.cursor()
    
    # Query to join the tables and get all photos for this specific person
    cursor.execute('''
        SELECT i.file_path 
        FROM Images i
        JOIN Image_Faces map ON i.image_id = map.image_id
        WHERE map.grab_id = ?
    ''', (grab_id,))
    
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return jsonify({"error": "No images found for this ID"}), 404
        
    # Extract just the file paths into a simple list
    image_paths = [row[0] for row in rows]
    
    return jsonify({
        "status": "success", 
        "grab_id": grab_id, 
        "images": image_paths
    })

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(host='127.0.0.1', port=8000)