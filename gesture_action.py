import pyautogui


class GestureAction:

    def perform_action(self, gesture):

        if gesture == "THUMBS UP":
            pyautogui.press("volumeup")

        elif gesture == "THUMBS DOWN":
            pyautogui.press("volumedown")

        elif gesture == "VICTORY":
            pyautogui.hotkey("win", "shift", "s")

        elif gesture == "OPEN PALM":
            pyautogui.press("space")

        elif gesture == "OK":
            pyautogui.hotkey("win", "r")

        elif gesture == "FIST":
            print("Gesture control stopped")