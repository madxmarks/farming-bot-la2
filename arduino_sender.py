# arduino_sender.py
import serial

class ArduinoSender:
    def __init__(self, port='COM5', baudrate=9600):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
        except serial.SerialException as e:
            print(f"[Ошибка] Не удалось подключиться к Ардуино: {e}")
            self.ser = None

    def send_key(self, key):
        if self.ser and self.ser.is_open:
            try:
                self.ser.write((key + '\n').encode('utf-8'))
            except serial.SerialException as e:
                print(f"[Ошибка] Не удалось отправить ключ: {e}")
