# hp_detector.py
import pyautogui
import numpy as np
import cv2

class HPDetector:
    def __init__(self, region):
        self.region = region

    def get_hp_percentage(self):
        # Получаем новый скриншот области
        screenshot = pyautogui.screenshot(region=self.region)
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Преобразуем в HSV для лучшей фильтрации цвета
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Цвет HP: светло-красный — нужно откорректировать по факту
        lower_hp = np.array([0, 70, 120])     # Нижний порог (примерный красный)
        upper_hp = np.array([10, 255, 255])   # Верхний порог

        mask = cv2.inRange(hsv, lower_hp, upper_hp)

        # Ищем контуры красной области
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return 0.0

        # Ищем наибольшую по ширине область — предположительно ХП
        max_width = 0
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if w > max_width:
                max_width = w

        full_width = mask.shape[1]  # Общая ширина полоски
        hp_percentage = (max_width / full_width) * 100

        return max(0.0, min(hp_percentage, 100.0))
