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


    # ==============================
    # MIRROR CAMERA
    # ==============================

    frame = cv2.flip(frame, 1)

    # Get frame size
    height, width = frame.shape[:2]


    # ==============================
    # DETECT HAND
    # ==============================

    frame, hands = detector.find_hands(frame)


    # ==============================
    # DEFAULT VALUES
    # ==============================

    gesture = "NO HAND DETECTED"
    stable_gesture = "UNKNOWN"

    color = (180, 180, 180)


    # ==============================
    # IF HAND DETECTED
    # ==============================

    if hands:

        # Get first detected hand
        landmarks = hands[0]


        # ==============================
        # DETECT GESTURE
        # ==============================

        gesture = gesture_controller.detect_gesture(
            landmarks
        )


        # ==============================
        # STABLE GESTURE
        # ==============================

        stable_gesture = gesture_controller.get_stable_gesture(
            gesture
        )


        # ==============================
        # DIFFERENT COLORS
        # OpenCV uses BGR
        # ==============================

        if gesture == "OPEN PALM":

            color = (0, 255, 0)      # Green

        elif gesture == "FIST":

            color = (0, 0, 255)      # Red

        elif gesture == "THUMBS UP":

            color = (255, 0, 0)      # Blue

        elif gesture == "THUMBS DOWN":

            color = (0, 165, 255)    # Orange

        elif gesture == "VICTORY":

            color = (0, 255, 255)    # Yellow

        elif gesture == "OK":

            color = (255, 0, 255)    # Purple

        else:

            color = (0, 165, 255)    # Orange


        # ==============================
        # HAND BOUNDING BOX
        # ==============================

        points_x = []
        points_y = []


        for point in landmarks:

            points_x.append(
                int(point.x * width)
            )

            points_y.append(
                int(point.y * height)
            )


        # Bounding box coordinates
        x_min = max(
            min(points_x) - 20,
            0
        )

        y_min = max(
            min(points_y) - 20,
            0
        )

        x_max = min(
            max(points_x) + 20,
            width
        )

        y_max = min(
            max(points_y) + 20,
            height
        )


        # Draw bounding box
        cv2.rectangle(
            frame,
            (x_min, y_min),
            (x_max, y_max),
            color,
            2
        )


        # Gesture name above hand
        cv2.putText(
            frame,
            gesture,
            (x_min, max(y_min - 10, 30)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2
        )


    # ==============================
    # NO HAND DETECTED
    # ==============================

    else:

        gesture_controller.gesture_history.clear()


    # ==============================
    # TOP LABEL BACKGROUND
    # ==============================

    cv2.rectangle(
        frame,
        (0, 0),
        (430, 90),
        (30, 30, 30),
        -1
    )


    # ==============================
    # MAIN GESTURE TEXT
    # ==============================

    cv2.putText(
        frame,
        gesture,
        (20, 55),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        color,
        2
    )


    # ==============================
    # COLOR INDICATOR
    # ==============================

    cv2.circle(
        frame,
        (390, 45),
        16,
        color,
        -1
    )


    # ==============================
    # BOTTOM INSTRUCTION
    # ==============================

    cv2.rectangle(
        frame,
        (0, height - 60),
        (width, height),
        (30, 30, 30),
        -1
    )

    cv2.putText(
        frame,
        "Show a hand gesture | Q = Quit",
        (20, height - 22),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
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