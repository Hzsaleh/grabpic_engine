import os
import sqlite3
import face_recognition
import numpy as np
import pickle

def ingest_images():
    print("Connecting to database...")
    conn = sqlite3.connect('grabpic.db')
    cursor = conn.cursor()
    
    image_folder = 'raw_images'
    if not os.path.exists(image_folder):
        print(f"Error: Could not find the '{image_folder}' folder.")
        return

    # Fetch existing faces from the database so we can compare new ones against them
    cursor.execute("SELECT grab_id, face_encoding FROM Faces")
    existing_faces = cursor.fetchall()
    known_encodings = []
    known_ids = []
    
    for face in existing_faces:
        known_ids.append(face[0])
        # We use pickle to convert the stored database bytes back into a mathematical array
        known_encodings.append(pickle.loads(face[1]))

    print(f"Scanning folder: {image_folder}...")
    for filename in os.listdir(image_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            filepath = os.path.join(image_folder, filename)
            
            # Check if we already processed this exact image
            cursor.execute("SELECT image_id FROM Images WHERE file_path = ?", (filepath,))
            if cursor.fetchone():
                print(f"Skipping {filename}, already processed.")
                continue

            print(f"Processing {filename}...")
            
            # Save the image path to the database
            cursor.execute("INSERT INTO Images (file_path) VALUES (?)", (filepath,))
            image_id = cursor.lastrowid
            
            # Load the image and find all faces in it
            image = face_recognition.load_image_file(filepath)
            encodings = face_recognition.face_encodings(image)
            
            if not encodings:
                print(f"  -> No faces found in {filename}.")
                continue

            for encoding in encodings:
                grab_id = None
                
                # If we have known faces, compare this new face to them
                if known_encodings:
                    matches = face_recognition.compare_faces(known_encodings, encoding, tolerance=0.5)
                    if True in matches:
                        first_match_index = matches.index(True)
                        grab_id = known_ids[first_match_index]
                
                # If it's a completely new face
                if grab_id is None:
                    # Convert the math array into bytes to save in SQLite
                    encoding_bytes = pickle.dumps(encoding)
                    cursor.execute("INSERT INTO Faces (face_encoding) VALUES (?)", (encoding_bytes,))
                    grab_id = cursor.lastrowid
                    
                    # Add to our running list so we recognize them in the next photo
                    known_encodings.append(encoding)
                    known_ids.append(grab_id)
                    print(f"  -> Found NEW face! Assigned grab_id: {grab_id}")
                else:
                    print(f"  -> Found KNOWN face! Matched existing grab_id: {grab_id}")
                    
                # Link the face to the image
                cursor.execute("INSERT INTO Image_Faces (image_id, grab_id) VALUES (?, ?)", (image_id, grab_id))
    
    conn.commit()
    conn.close()
    print("Finished processing all images!")

if __name__ == '__main__':
    ingest_images()