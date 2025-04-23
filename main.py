import tkinter as tk
from tkinter import ttk
import cv2
import hand_tracking as ht  # Import the hand tracking module
import threading
import pyautogui
import numpy as np
import time

class GestureControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gesture Control")
        self.root.configure(bg="#2E2E2E")  # Dark background

        # Create a label
        self.label = tk.Label(root, text="Select Actions and Assign Gestures", bg="#2E2E2E", fg="white")
        self.label.pack(pady=10)

        # Action selection
        self.action_label = tk.Label(root, text="Select Action:", bg="#2E2E2E", fg="white")
        self.action_label.pack(pady=5)

        self.action_var = tk.StringVar()
        self.action_menu = ttk.Combobox(root, textvariable=self.action_var)
        self.action_menu['values'] = ("Click", "Move", "Zoom In", "Zoom Out")
        self.action_menu.pack(pady=5)
        self.action_menu.set("Select Action")

        # Gesture selection
        self.gesture_label = tk.Label(root, text="Select Gesture:", bg="#2E2E2E", fg="white")
        self.gesture_label.pack(pady=5)

        self.gesture_var = tk.StringVar()
        self.gesture_menu = ttk.Combobox(root, textvariable=self.gesture_var)
        self.gesture_menu['values'] = ("One Finger", "Two Fingers", "Palm")
        self.gesture_menu.pack(pady=5)
        self.gesture_menu.set("Select Gesture")

        # Button to assign gesture to action
        self.assign_button = tk.Button(root, text="Assign Gesture to Action", command=self.assign_gesture, bg="#4CAF50", fg="white")
        self.assign_button.pack(pady=20)

        # Button to save settings
        self.save_button = tk.Button(root, text="Save Settings", command=self.save_settings, bg="#4CAF50", fg="white")
        self.save_button.pack(pady=5)

        # Text area to display assignments
        self.assignment_area = tk.Text(root, height=10, width=50, bg="#3E3E3E", fg="white")
        self.assignment_area.pack(pady=10)

        self.assignments = {}

        # Start the hand tracking in a separate thread
        self.tracking_thread = threading.Thread(target=self.start_hand_tracking)
        self.tracking_thread.daemon = True
        self.tracking_thread.start()

    def assign_gesture(self):
        action = self.action_var.get()
        gesture = self.gesture_var.get()
        if action and gesture:
            self.assignments[action] = gesture
            self.assignment_area.insert(tk.END, f"{action} -> {gesture}\n")
        else:
            print("Please select both an action and a gesture.")

    def save_settings(self):
        with open("gesture_settings.txt", "w") as file:
            for action, gesture in self.assignments.items():
                file.write(f"{action}: {gesture}\n")
        print("Settings saved!")

    def start_hand_tracking(self):
        # Camera Settings
        wCam, hCam = 640, 480
        frameR = 100  # Frame Reduction
        smoothening = 7

        pTime = 0
        plocX, plocY = 0, 0
        clocX, clocY = 0, 0

        cap = cv2.VideoCapture(1)  # Use 0 for built-in camera
        cap.set(3, wCam)
        cap.set(4, hCam)

        detector = ht.handDetector(maxHands=1)
        wScr, hScr = pyautogui.size()  # Get screen size

        while True:
            # 1. Capture Frame
            success, img = cap.read()
            if not success:
                continue

            img = detector.findHands(img)
            lmList, _ = detector.findPosition(img)

            # 2. Get Tip of Index & Middle Finger
            if len(lmList) != 0:
                x1, y1 = lmList[8][1:]  # Index finger tip
                x2, y2 = lmList[12][1:]  # Middle finger tip

                # 3. Check which fingers are up
                fingers = detector.fingersUp()

                # 4. Draw Rectangle on Screen
                cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

                # 5. Moving Mode
                if fingers[1] == 1:  # Index finger up
                    if "Move" in self.assignments:
                        if self.assignments["Move"] == "One Finger":
                            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

                            clocX = plocX + (x3 - plocX) / smoothening
                            clocY = plocY + (y3 - plocY) / smoothening

                            pyautogui.moveTo(wScr - clocX, clocY)  # Move cursor
                            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                            plocX, plocY = clocX, clocY

                if fingers[1] == 1 and fingers[2] == 1:  # Both fingers up
                    if "Move" in self.assignments:
                        if self.assignments["Move"] == "Two Fingers":
                            x3 = np.interp(x2, (frameR, wCam - frameR), (0, wScr))
                            y3 = np.interp(y2, (frameR, hCam - frameR), (0, hScr))

                            clocX = plocX + (x3 - plocX) / smoothening
                            clocY = plocY + (y3 - plocY) / smoothening

                            pyautogui.moveTo(wScr - clocX, clocY)  # Move cursor
                            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
                            plocX, plocY = clocX, clocY

                # 6. Clicking Mode
                if fingers[1] == 1 and fingers[2] == 1:  # Both index and middle fingers up
                    if "Click" in self.assignments:
                        if self.assignments["Click"] == "Two Fingers":
                            length, img, lineInfo = detector.findDistance(8, 12, img)

                            if length < 40:  # If fingers are close enough
                                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                                pyautogui.click()  # Simulate mouse click

                if fingers[1] == 1:  # Index finger up
                    if "Click" in self.assignments:
                        if self.assignments["Click"] == "One Finger":
                            length, img, lineInfo = detector.findDistance(8, 12, img)

                            if length < 40:  # If fingers are close enough
                                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                                pyautogui.click()  # Simulate mouse click

                # 7. Zoom In/Out Mode (Palm Gesture)
                if fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:  # Palm open
                    if "Zoom In" in self.assignments and self.assignments["Zoom In"] == "Palm":
                        pyautogui.hotkey('ctrl', '+')  # Simulate zoom in
                    elif "Zoom Out" in self.assignments and self.assignments["Zoom Out"] == "Palm":
                        pyautogui.hotkey('ctrl', '-')  # Simulate zoom out

            # 8. Calculate Frame Rate (FPS)
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

            # 9. Display Output
            cv2.imshow("Image", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = tk.Tk()
    app = GestureControlApp(root)
    root.mainloop()