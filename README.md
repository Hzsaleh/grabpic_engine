# Grabpic Intelligent Identity & Retrieval Engine

A high-performance image processing backend designed for large-scale events. It uses facial recognition to automatically group images and provides a secure "Selfie-as-a-Key" retrieval system.

## 🏗️ Architecture Design & Schema
**Tech Stack:** Python, Flask, SQLite, `face_recognition` 

**System Flow:**
1. **Discovery & Transformation (Ingestion Engine):** Scans a local storage folder (`raw_images`), extracts mathematical facial encodings using C++ models, and persists them into a relational database.
2. **Web API:** A lightweight Flask server handling selfie authentication and search token retrieval.

**Relational Database Schema:**
The database maps one image to potentially many users.
* **`Images` Table:** `image_id` (PK), `file_path`
* **`Faces` Table:** `grab_id` (PK), `face_encoding` (BLOB)
* **`Image_Faces` Table:** `image_id` (FK), `grab_id` (FK) -> Many-to-Many mapping.

## 🚀 Setup & Installation
1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   
2.Install dependencies (requires specific setuptools version for model compatibility):
   ```bash
   pip install flask face_recognition numpy setuptools==76.0.0

⚙️ Running the Engine
Step 1: Run the Ingestion Engine (Ensure you have a raw_images folder with photos)
   ```bash
python3 ingest.py

Step 2: Start the Web API
   ```bash
python3 app.py
📖 API Documentation & cURL Tests
1. Selfie Authentication
Authenticates a user via an image file and returns their authorizer grab_id.

Endpoint: POST /authenticate

cURL Command:
   ```bash
curl -X POST -F "file=@test_selfie.jpg" [http://127.0.0.1:8000/authenticate](http://127.0.0.1:8000/authenticate)

2. Data Extraction
Fetches all indexed images for a specific user.

Endpoint: GET /images/<grab_id>

cURL Command:

curl -X GET [http://127.0.0.1:8000/images/1](http://127.0.0.1:8000/images/1)
