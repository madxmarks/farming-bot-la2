import tkinter as tk
from tkinter import ttk
from window_selector import list_windows
from region_selector import RegionSelector
from app_controller import AppController

class AppUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HP Tracker")
        self.root.geometry("700x700")

        self.controller = AppController(update_ui_callback=self.update_hp_label)

        # UI
        self.window_var = tk.StringVar()
        self.dropdown = ttk.Combobox(root, textvariable=self.window_var, state="readonly")
        self.dropdown.pack(pady=5)
        self.refresh_windows()

        tk.Button(root, text="Обновить окна", command=self.refresh_windows).pack()
        tk.Button(root, text="Выделить область", command=self.select_region).pack(pady=5)

        self.hp_label = tk.Label(root, text="HP: ???", font=("Arial", 22))
        self.hp_label.pack(pady=20)

        self.key_frame = tk.Frame(root)
        self.key_frame.pack(pady=10)
        self.render_keys()

        tk.Button(root, text="Добавить клавишу", command=self.add_key_prompt).pack(pady=10)
        
        tk.Button(root, text="Старт", command=self.start_bot).pack(pady=10)
        tk.Button(root, text="Стоп", command=self.stop_bot).pack(pady=5)

    def refresh_windows(self):
        self.windows = list_windows()
        titles = [t for t, _ in self.windows]
        self.dropdown["values"] = titles
        if titles:
            self.window_var.set(titles[0])

    def select_region(self):
        index = self.dropdown.current()
        if index < 0 or index >= len(self.windows):
            print("Окно не выбрано")
            return

        _, handle = self.windows[index]
        self.controller.set_window_handle(handle)
        self.controller.activate_window()

        selector = RegionSelector(callback=self.controller.set_region)
        selector.start()

    def update_hp_label(self, hp_value):
        self.hp_label.config(text=f"HP: {hp_value:.2f}%")

    def render_keys(self):
        for widget in self.key_frame.winfo_children():
            widget.destroy()

        for binding in self.controller.key_manager.get_keys():
            row = tk.Frame(self.key_frame)
            row.pack(anchor="w", pady=2)

            if binding.condition_type == 'lt':
                text = f"{binding.key} — если HP < {binding.threshold}%, раз в {binding.interval}с"
            elif binding.condition_type == 'gt':
                text = f"{binding.key} — если HP > {binding.threshold}%, раз в {binding.interval}с"
            else:
                text = f"{binding.key} — каждые {binding.interval}с (без условия)"

            label = tk.Label(row, text=text)
            label.pack(side="left")

            delete_btn = tk.Button(row, text="Удалить", command=lambda b=binding: self.delete_key(b))
            delete_btn.pack(side="left", padx=5)

    def delete_key(self, binding):
        self.controller.key_manager.remove_binding(binding)
        self.render_keys()

    def add_key_prompt(self):
        popup = tk.Toplevel(self.root)
        popup.title("Добавить клавишу")

        tk.Label(popup, text="Клавиша:").pack()
        key_entry = tk.Entry(popup)
        key_entry.pack()

        tk.Label(popup, text="Интервал (минуты):").pack()
        minutes_entry = tk.Entry(popup)
        minutes_entry.pack()

        tk.Label(popup, text="Интервал (секунды):").pack()
        seconds_entry = tk.Entry(popup)
        seconds_entry.pack()

        condition_var = tk.StringVar(value="none")
        tk.Label(popup, text="Условие:").pack()
        ttk.Combobox(popup, textvariable=condition_var, state="readonly",
                    values=["none", "HP < порог", "HP > порог"]).pack()

        tk.Label(popup, text="Порог HP (%):").pack()
        threshold_entry = tk.Entry(popup)
        threshold_entry.pack()

        def save():
            key = key_entry.get()
            try:
                minutes = int(minutes_entry.get() or 0)
                seconds = int(seconds_entry.get() or 0)
                interval = minutes * 60 + seconds

                condition_type = condition_var.get()
                if condition_type == "none":
                    self.controller.key_manager.add_key(key, minutes, seconds)
                else:
                    threshold = float(threshold_entry.get())
                    if condition_type == "HP < порог":
                        self.controller.key_manager.add_key(key, minutes, seconds, "lt", threshold)
                    elif condition_type == "HP > порог":
                        self.controller.key_manager.add_key(key, minutes, seconds, "gt", threshold)

                self.render_keys()
                popup.destroy()
            except ValueError:
                pass

        tk.Button(popup, text="Сохранить", command=save).pack()

    def start_bot(self):
        if not self.controller.is_running:
            self.controller.start_threads()

    def stop_bot(self):
        if self.controller.is_running:
            self.controller.stop_threads()