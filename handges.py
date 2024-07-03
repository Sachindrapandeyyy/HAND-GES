import cv2 as cv
import mediapipe as mp
import pyautogui
import os
import time
from pynput.mouse import Controller, Button
from kit import distance

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Open webcam
cap = cv.VideoCapture(0)

# Variables for gesture control
mouse = Controller()
snap_count = 0

# Helper function to perform actions based on gestures
def perform_actions(gesture):
    if gesture == "close_hands":
        pyautogui.hotkey('alt', 'f4')
    elif gesture == "shutdown_pc":
        os.system("shutdown /s /t 1")
    elif gesture == "left_click":
        pyautogui.click()
    elif gesture == "lock_window":
        pyautogui.hotkey('win', 'l')
    elif gesture == "scroll_up":
        pyautogui.scroll(10)  # Scroll up 3 units
    elif gesture == "scroll_down":
        pyautogui.scroll(-10)  # Scroll down 3 units
    elif gesture == "zoom_in":
        pyautogui.hotkey('ctrl', '+')
    elif gesture == "zoom_out":
        pyautogui.hotkey('ctrl', '-')
    elif gesture == "switch_tabs_right":
        pyautogui.hotkey('ctrl', 'tab')
    elif gesture == "switch_tabs_left":
        pyautogui.hotkey('ctrl', 'shift', 'tab')
    elif gesture == "volume_increase":
        pyautogui.press('volumeup')
    elif gesture == "volume_decrease":
        pyautogui.press('volumedown')
    elif gesture == "screen_capture":
        pyautogui.hotkey('win', 'shift', 's')  # Windows screenshot shortcut
    # Add more actions as needed

# Main loop for gesture control
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Convert frame to RGB for MediaPipe
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get landmarks
            landmarks = [[lm.x, lm.y] for lm in hand_landmarks.landmark]
            
            # Calculate gesture parameters
            thumb_tip = landmarks[4]
            index_tip = landmarks[8]
            middle_tip = landmarks[12]

            # Check for gestures
            thumb_index_dist = distance(thumb_tip, index_tip)
            thumb_middle_dist = distance(thumb_tip, middle_tip)

            # Perform actions based on gestures
            if thumb_index_dist < 0.05 and thumb_middle_dist < 0.05:
                perform_actions("close_hands")
            elif thumb_index_dist < 0.05 and thumb_middle_dist > 0.2:
                perform_actions("shutdown_pc")
            elif len(results.multi_hand_landmarks) == 1 and results.multi_handedness[0].classification[0].label == 'Right' and thumb_tip[0] > index_tip[0]:
                perform_actions("left_click")
            elif thumb_index_dist < 0.05 and thumb_middle_dist < 0.05:
                snap_count += 1
                if snap_count == 3:
                    perform_actions("lock_window")
            elif thumb_tip[1] > index_tip[1] and middle_tip[1] > index_tip[1]:
                perform_actions("scroll_up")
            elif thumb_tip[1] < index_tip[1] and middle_tip[1] < index_tip[1]:
                perform_actions("scroll_down")
            elif thumb_tip[0] < index_tip[0] and middle_tip[0] < index_tip[0]:
                perform_actions("zoom_in")
            elif thumb_tip[0] > index_tip[0] and middle_tip[0] > index_tip[0]:
                perform_actions("zoom_out")
            elif thumb_tip[0] < index_tip[0] and middle_tip[0] > index_tip[0]:
                perform_actions("switch_tabs_right")
            elif thumb_tip[0] > index_tip[0] and middle_tip[0] < index_tip[0]:
                perform_actions("switch_tabs_left")
            elif thumb_tip[1] > index_tip[1] and middle_tip[1] < index_tip[1]:
                perform_actions("volume_increase")
            elif thumb_tip[1] < index_tip[1] and middle_tip[1] > index_tip[1]:
                perform_actions("volume_decrease")
            elif thumb_tip[0] < index_tip[0] and thumb_tip[1] > index_tip[1] and middle_tip[0] > index_tip[0] and middle_tip[1] < index_tip[1]:
                perform_actions("screen_capture")
            # Add more conditions for other gestures

            # Draw hand landmarks
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv.imshow('Hand Gesture Control', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

    # Delay to reduce computation frequency
    time.sleep(0.03)  # Decreased delay for more responsive interaction

hands.close()
cap.release()
cv.destroyAllWindows()

