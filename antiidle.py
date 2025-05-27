import threading
import time
import customtkinter as ctk
import keyboard

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AntiIdleApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Roblox Anti-Idle")
        self.geometry("250x100")
        self.resizable(False, False)

        # State flag and settings
        self.running = False
        self.interval = 300
        self.press_duration_space = 0.5
        self.press_duration_w = 0.3
        self.key_space = 'space'
        self.key_w = 'w'

        # Build UI
        self.create_widgets()

        # Hotkey to toggle start/stop
        keyboard.add_hotkey('F7', self.toggle)

    def create_widgets(self):
        frame = ctk.CTkFrame(self)
        frame.pack(padx=8, pady=8)

        self.toggle_btn = ctk.CTkButton(
            frame,
            text="Start (F7)",
            fg_color="green",
            command=self.toggle
        )
        self.toggle_btn.pack(pady=(0, 4))
        ctk.CTkLabel(
            frame,
            text="Press F7 or button to toggle"
        ).pack()

    def start(self):
        if not self.running:
            self.running = True
            self.toggle_btn.configure(text="Stop (F7)", fg_color="red")
            threading.Thread(target=self.run_loop, daemon=True).start()

    def stop(self):
        if self.running:
            self.running = False
            self.toggle_btn.configure(text="Start (F7)", fg_color="green")

    def toggle(self):
        if self.running:
            self.stop()
        else:
            self.start()

    def run_loop(self):
        while self.running:
            # Press and hold space
            keyboard.press(self.key_space)
            time.sleep(self.press_duration_space)
            keyboard.release(self.key_space)

            # Press and hold w for 0.30 seconds
            keyboard.press(self.key_w)
            time.sleep(self.press_duration_w)
            keyboard.release(self.key_w)

            # Wait remaining interval
            time.sleep(self.interval - self.press_duration_space - self.press_duration_w)

if __name__ == "__main__":
    app = AntiIdleApp()
    app.mainloop()