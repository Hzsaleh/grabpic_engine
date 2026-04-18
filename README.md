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
