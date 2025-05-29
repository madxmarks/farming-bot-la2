import threading
import time
from utils.hp_detector import HPDetector
from utils.key_binding import KeyManager
from utils.arduino_sender import ArduinoSender
import win32gui

class AppController:
    def __init__(self, update_ui_callback):
        self.region = None
        self.hp_detector = None
        self.hp_thread_running = False
        self.hp = 0.0
        self.is_running = False
        self.window_handle = None

        self.arduino = ArduinoSender(port='COM5')
        self.key_manager = KeyManager(self.arduino)
        self.update_ui_callback = update_ui_callback  # передаём ссылку для обновления UI

    def set_region(self, region):
        if region is None:
            print("Выделение отменено")
            return

        self.region = region
        self.hp_detector = HPDetector(region)

        if not self.hp_thread_running:
            self.hp_thread_running = True
            threading.Thread(target=self.monitor_hp, daemon=True).start()
            threading.Thread(target=self.key_loop, daemon=True).start()

    def monitor_hp(self):
        while self.is_running:
            if self.hp_detector:
                self.hp = self.hp_detector.get_hp_percentage()
                self.update_ui_callback(self.hp)
            time.sleep(0.5)

    def key_loop(self):
        while self.is_running:
            self.key_manager.update(self.hp)
            time.sleep(0.1)

    def set_window_handle(self, handle):
        self.window_handle = handle

    def activate_window(self):
        import win32gui
        if self.window_handle:
            win32gui.ShowWindow(self.window_handle, 5)  # SW_SHOW
            win32gui.SetForegroundWindow(self.window_handle)

    def start_threads(self):
        if not self.hp_detector:
            print("HPDetector не установлен")
            return
        self.is_running = True
        print("Бот запущен")
        threading.Thread(target=self.monitor_hp, daemon=True).start()
        threading.Thread(target=self.key_loop, daemon=True).start()

    def stop_threads(self):
        self.is_running = False
        print("Бот остановлен")