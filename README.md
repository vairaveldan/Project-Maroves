# MAROVES: Intelligent Obstruction Management System for Rovers

Welcome to the official repository for **MAROVES** – a final-year engineering project focused on building an intelligent system to detect and remove obstructions from rover wheels using computer vision and robotics.

This project, titled **"Design and Development of an Intelligent Obstruction Management System for Rovers,"** aims to enhance planetary rover autonomy and resilience by addressing the real-world issue of lodged stones using machine learning and a robotic arm.

## 🌍 Problem Statement

> During its Mars mission, NASA’s Perseverance rover had a stone lodged in its wheel for 437 days, causing minor damage. If not managed, such obstructions can threaten the stability and success of long-term planetary exploration.

## 🧠 Proposed Solution

Our system detects and removes lodged stones from rover wheels using a Raspberry Pi camera, a TensorFlow CNN model, and a robotic arm. The solution integrates real-time detection, classification, and mechanical removal to protect the rover’s structure and improve operational longevity.

## ⚙️ Methodology

- **Image Capture:** Raspberry Pi camera captures wheel images.
- **Image Processing & Detection:** TensorFlow/Keras CNN detects obstruction using a pre-trained model.
- **Signal Transmission:** Detection signal sent to Arduino via GPIO.
- **Robotic Arm Activation:** Arduino executes predefined servo motor sequence to remove the stone.

## 🧪 Components

| Component              | Description                      |
|------------------------|----------------------------------|
| Raspberry Pi 1 Model B+| Controls image processing & logic|
| RPi 5MP Camera Module  | Captures wheel images            |
| Arduino Mega           | Controls servo motors            |
| MG995 Servo Motors     | Moves robotic arm                |
| TensorFlow/Keras CNN   | Detects stone obstructions       |
| OpenCV                 | Preprocessing image data         |

## 📁 Folder Overview

- `main_project/` - Full implementation (data collection, model, robotic arm)
- `mini_project/` - Rock classification model
- `docs/`         - Technical writeups (problem, solution, diagrams)

## 🧰 Software Stack

- Python 3
- OpenCV
- TensorFlow / Keras
- Paramiko (SSH communication)
- Arduino IDE / C++

## 📂 Code Structure

- `1)Image Capturing and Prediction To Trigger Robotic Arm if stone detected.py`: Captures and classifies images. Triggers robotic arm if stone is found.
- `2)program.py`: Controls GPIO pin to send signal to Arduino.
- `3)Robotic Arm Controller.ino`: Arduino code to run the robotic arm.
- `keras_model.h5`: Trained CNN model.
- `labels.txt`: Class names.

## 📊 Dataset

Custom dataset created manually with Raspberry Pi:
- `Stone` images: various positions and angles.
- `Empty` images: no stone in wheel.

## 📸 How It Works

1. A camera on the rover takes pictures of the wheel.
2. Raspberry Pi uses a trained machine learning model to check for stones.
3. If a stone is detected, it sends a signal to Arduino.
4. Arduino moves a robotic arm to remove the stone by predefined action according to each 6 wheels.

## 🚀 Goal

Help Mars rovers remove wheel obstructions automatically, preventing mission failure.

## 🔐 Security Note

This is a college-level academic project. SSH passwords are exposed for simplicity. If adapting for production or public use, implement secure authentication.

## 📬 Contact

For questions or collaborations, reach out to [vair.71772114148@gct.ac.in].
