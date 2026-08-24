import cv2

from hand_detector import HandDetector
from gesture_controller import GestureController


# ==============================
# START CAMERA
# ==============================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera could not be opened!")
    exit()


# ==============================
# CREATE OBJECTS
# ==============================

detector = HandDetector()
gesture_controller = GestureController()


# ==============================
# WINDOW
# ==============================

window_name = "NexaGesture AI - Hand Recognition"

cv2.namedWindow(
    window_name,
    cv2.WINDOW_NORMAL
)

cv2.resizeWindow(
    window_name,
    1000,
    700
)


# ==============================
# MAIN LOOP
# ==============================

while True:

    success, frame = cap.read()

    if not success:
        print("Failed to read camera!")
        break


    # Mirror camera
    frame = cv2.flip(frame, 1)


    # ==============================
    # DETECT HAND
    # ==============================

    frame, hands = detector.find_hands(frame)


    # Default values
    gesture = "NO HAND DETECTED"

    color = (180, 180, 180)


    # ==============================
    # IF HAND DETECTED
    # ==============================

    if hands:

        # Detect gesture
        gesture = gesture_controller.detect_gesture(
            hands[0]
        )


        # ==============================
        # DIFFERENT COLORS
        # OpenCV = BGR
        # ==============================

        if gesture == "OPEN PALM":

            color = (0, 255, 0)      # Green


        elif gesture == "FIST":

            color = (0, 0, 255)      # Red


        elif gesture == "THUMBS UP":

            color = (255, 0, 0)      # Blue


        elif gesture == "VICTORY":

            color = (0, 255, 255)    # Yellow


        elif gesture == "OK":

            color = (255, 0, 255)    # Purple


        else:

            color = (0, 165, 255)    # Orange


    # ==============================
    # TOP LABEL BACKGROUND
    # ==============================

    cv2.rectangle(
        frame,
        (0, 0),
        (420, 100),
        (30, 30, 30),
        -1
    )


    # ==============================
    # GESTURE TEXT
    # ==============================

    cv2.putText(
        frame,
        gesture,
        (25, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        color,
        3
    )


    # ==============================
    # COLOR INDICATOR
    # ==============================

    cv2.circle(
        frame,
        (380, 50),
        18,
        color,
        -1
    )


    # ==============================
    # INSTRUCTIONS
    # ==============================

    cv2.putText(
        frame,
        "Show a hand gesture",
        (20, frame.shape[0] - 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )


    # ==============================
    # DISPLAY
    # ==============================

    cv2.imshow(
        window_name,
        frame
    )


    # ==============================
    # PRESS Q TO QUIT
    # ==============================

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ==============================
# CLOSE CAMERA
# ==============================

cap.release()

cv2.destroyAllWindows()