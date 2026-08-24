import cv2
import mediapipe as mp


class HandDetector:

    def __init__(self):
        self.BaseOptions = mp.tasks.BaseOptions
        self.HandLandmarker = mp.tasks.vision.HandLandmarker
        self.HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
        self.VisionRunningMode = mp.tasks.vision.RunningMode

        options = self.HandLandmarkerOptions(
            base_options=self.BaseOptions(
                model_asset_path="models/hand_landmarker.task"
            ),
            running_mode=self.VisionRunningMode.IMAGE,
            num_hands=1
        )

        self.detector = self.HandLandmarker.create_from_options(options)

    def find_hands(self, frame):

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        result = self.detector.detect(mp_image)

        if result.hand_landmarks:

            for hand_landmarks in result.hand_landmarks:

                for landmark in hand_landmarks:

                    h, w, _ = frame.shape

                    x = int(landmark.x * w)
                    y = int(landmark.y * h)

                    cv2.circle(
                        frame,
                        (x, y),
                        5,
                        (0, 120, 255),
                        -1
                    )

                # Draw connections
                connections = mp.tasks.vision.HandLandmarksConnections.HAND_CONNECTIONS

                for connection in connections:
                    start = hand_landmarks[connection.start]
                    end = hand_landmarks[connection.end]

                    h, w, _ = frame.shape

                    start_point = (
                        int(start.x * w),
                        int(start.y * h)
                    )

                    end_point = (
                        int(end.x * w),
                        int(end.y * h)
                    )

                    cv2.line(
                        frame,
                        start_point,
                        end_point,
                        (255, 120, 0),
                        2
                    )

        return frame, result.hand_landmarks