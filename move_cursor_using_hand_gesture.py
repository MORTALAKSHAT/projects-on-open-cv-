import cv2
import mediapipe as mp
import pyautogui

capture_hand = mp.solutions.hands.Hands()
drawing_option = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()
camera = cv2.VideoCapture(0)

x1 = y1 = x2 = y2 = 0

while True:
    _, image = camera.read()
    image = cv2.flip(image, 1)
    image_height, image_width, _ = image.shape
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    output_hands = capture_hand.process(rgb_image)
    all_hands = output_hands.multi_hand_landmarks

    if all_hands:
        for hand in all_hands:
            drawing_option.draw_landmarks(image, hand)
            one_hand_landmarks = hand.landmark

            for id, lm in enumerate(one_hand_landmarks):
                x = int(lm.x * image_width)
                y = int(lm.y * image_height)

                if id == 8:  # Index finger tip
                    mouse_x = int(screen_width * x / image_width)
                    mouse_y = int(screen_height * y / image_height)
                    cv2.circle(image, (x, y), 15, (0, 255, 255), cv2.FILLED)
                    pyautogui.moveTo(mouse_x, mouse_y)
                    x1, y1 = x, y

                if id == 4:  # Thumb tip
                    x2, y2 = x, y
                    cv2.circle(image, (x, y), 15, (0, 255, 255), cv2.FILLED)

        distance = abs(y2 - y1)
        print(distance)

        if distance < 20:
            pyautogui.click()
            print("Clicked!")

    cv2.imshow("Hand Movement Video Capture", image)

    key = cv2.waitKey(1)
    if key == 27:
        break

camera.release()
cv2.destroyAllWindows()
