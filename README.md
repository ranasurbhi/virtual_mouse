# Custom Gesture-Controlled Virtual Mouse

This project is a gesture-based virtual mouse system that allows users to interact with their computer using hand movements captured via webcam. The **novelty** of this project lies in its **customizable gesture control**—users can assign specific actions (like left-click, right-click, scroll, drag) to hand gestures of their choice.

---

## 🧠 Features

- 🖐️ Real-time hand tracking using webcam  
- 🖱️ Control mouse movement with hand position  
- 👆 Customizable gestures for different mouse actions  
- 🛠️ Smooth user experience with minimal latency  
- 🔒 No external hardware required—just a webcam

---

## 📌 Technologies Used

- **Programming Language:** Python  
- **Libraries:**  
  - `OpenCV` – for image processing  
  - `Mediapipe` – for accurate hand detection and tracking  
  - `PyAutoGUI` – for controlling mouse actions  
  - `Tkinter` (optional) – for the gesture-action mapping interface

---

## ⚙️ How It Works

1. The webcam captures hand gestures in real-time.
2. **MediaPipe** detects and tracks key points of the hand.
3. Based on gesture patterns (like number of fingers up), the system identifies the intended action.
4. Users can **customize which gesture triggers which action** using a simple interface.
5. **PyAutoGUI** executes the corresponding mouse command on screen.

---

## 🚀 Getting Started

### 1. Clone the Repository
### 2. Install Dependencies
### 3. Run the Application
