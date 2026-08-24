import math


class GestureController:

    def __init__(self):
        self.gesture_history = []

        # Stability settings
        self.required_frames = 8
        self.stable_gesture = "UNKNOWN"

        # Cooldown settings
        self.cooldown_frames = 15
        self.cooldown_counter = 0

    def is_finger_up(self, landmarks, tip_id, pip_id):
        return landmarks[tip_id].y < landmarks[pip_id].y

    def distance(self, p1, p2):
        return math.sqrt(
            (p1.x - p2.x) ** 2 +
            (p1.y - p2.y) ** 2
        )

    def detect_gesture(self, landmarks):

        thumb_tip = 4
        thumb_ip = 3

        index_tip = 8
        index_pip = 6

        middle_tip = 12
        middle_pip = 10

        ring_tip = 16
        ring_pip = 14

        pinky_tip = 20
        pinky_pip = 18

        # -------------------------
        # Finger states
        # -------------------------

        index_up = self.is_finger_up(
            landmarks, index_tip, index_pip
        )

        middle_up = self.is_finger_up(
            landmarks, middle_tip, middle_pip
        )

        ring_up = self.is_finger_up(
            landmarks, ring_tip, ring_pip
        )

        pinky_up = self.is_finger_up(
            landmarks, pinky_tip, pinky_pip
        )

        # -------------------------
        # THUMBS UP
        # -------------------------

        thumb_up = landmarks[thumb_tip].y < landmarks[thumb_ip].y

        if (
            thumb_up
            and not index_up
            and not middle_up
            and not ring_up
            and not pinky_up
        ):
            return "THUMBS UP"

        # -------------------------
        # THUMBS DOWN
        # -------------------------

        thumb_down = landmarks[thumb_tip].y > landmarks[thumb_ip].y

        if (
            thumb_down
            and not index_up
            and not middle_up
            and not ring_up
            and not pinky_up
        ):
            return "THUMBS DOWN"

        # -------------------------
        # OK
        # -------------------------

        thumb_index_distance = self.distance(
            landmarks[thumb_tip],
            landmarks[index_tip]
        )

        if (
            thumb_index_distance < 0.08
            and middle_up
            and ring_up
            and pinky_up
        ):
            return "OK"

        # -------------------------
        # OPEN PALM
        # -------------------------

        if (
            index_up
            and middle_up
            and ring_up
            and pinky_up
        ):
            return "OPEN PALM"

        # -------------------------
        # FIST
        # -------------------------

        if (
            not index_up
            and not middle_up
            and not ring_up
            and not pinky_up
        ):
            return "FIST"

        # -------------------------
        # VICTORY
        # -------------------------

        if (
            index_up
            and middle_up
            and not ring_up
            and not pinky_up
        ):
            return "VICTORY"

        return "UNKNOWN"

    # -------------------------
    # Stability checking
    # -------------------------

    def get_stable_gesture(self, gesture):

        self.gesture_history.append(gesture)

        if len(self.gesture_history) > self.required_frames:
            self.gesture_history.pop(0)

        # Check whether all recent frames
        # contain the same gesture
        if (
            len(self.gesture_history) == self.required_frames
            and len(set(self.gesture_history)) == 1
        ):
            self.stable_gesture = gesture

        return self.stable_gesture

    # -------------------------
    # Cooldown checking
    # -------------------------

    def can_execute(self):

        if self.cooldown_counter > 0:
            self.cooldown_counter -= 1
            return False

        self.cooldown_counter = self.cooldown_frames
        return True