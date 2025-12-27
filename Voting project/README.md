# AI-Powered Biometric Voter Integrity System
## Overview
This project implements a secure biometric voter authentication system that ensures **one-person-one-vote** using real-time face recognition, liveness detection, and fraud prevention.

The system verifies voters using facial biometrics, prevents spoofing attacks using blink-based liveness detection, and maintains a persistent audit trail using a database and logs.

## Key Features
- Face-based voter registration
- Real-time voter verification
- Blink-based liveness detection (anti-spoofing)
- Double-voting fraud prevention
- Persistent SQLite database
- Event logging and election analytics

## System Architecture
1. Webcam captures live video
2. MediaPipe detects face and facial landmarks
3. Facial landmarks converted into numerical embeddings
4. Embeddings compared using Euclidean distance
5. SQLite database verifies voter status
6. Logs record authentication and fraud events

## Technology Stack
- **Language:** Python
- **Face Detection & Landmarks:** MediaPipe
- **Computer Vision:** OpenCV
- **Database:** SQLite
- **Algorithms:** Euclidean Distance, Eye Aspect Ratio (EAR)
- **Security:** Liveness Detection, Audit Logs


