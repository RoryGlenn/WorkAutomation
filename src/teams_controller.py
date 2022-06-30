import pyautogui
import time

pyautogui.FAILSAFE = False

class TeamsController():
    def __init__(self, meeting_id, password):
        self.meeting_id = meeting_id
        self.password = password

    def main(self):
        # clicks on zoom logo in the task bar and opens it
        time.sleep(1)
        pyautogui.click(550, 800, duration=0.2)

        # clicks on join button
        time.sleep(2)
        pyautogui.click(x=550, y=317, clicks=2, interval=0.2)

        # types the meeting id
        pyautogui.typewrite(self.meeting_id,interval=0.06)

        # clicks the join button
        time.sleep(2)
        pyautogui.click(x=690, y=487)

        # types the password
        time.sleep(5)
        pyautogui.click(x=550, y=317, clicks=2)
        pyautogui.typewrite(self.password, interval=0.06)


        # clicks the join button
        time.sleep(1)
        pyautogui.click(x=690, y=487, clicks=1)

        # final joining
        time.sleep(5)
        pyautogui.click(x=900, y=590, clicks=2, interval=2)


# if __name__ == '__main__':
    # time.sleep(10)
    # zoom = ZoomOpener('9656400024', '123456')
    # zoom.main()