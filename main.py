
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import csv
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "keystrokes.csv")

os.makedirs(LOG_DIR, exist_ok=True)


class KeyloggerLab:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Keylogger Lab")
        self.root.geometry("650x480")
        self.root.resizable(False, False)

        self.recording = False

        self.create_ui()

    def create_ui(self):
        title = ttk.Label(
            self.root,
            text="KEYLOGGER LAB",
            font=("Segoe UI", 20, "bold")
        )
        title.pack(pady=15)

        self.status = ttk.Label(
            self.root,
            text="● STOPPED",
            foreground="red",
            font=("Segoe UI", 11, "bold")
        )
        self.status.pack(pady=5)

        ttk.Label(
            self.root,
            text="Ketik teks pengujian pada kolom berikut:"
        ).pack(pady=8)

        self.input_box = tk.Text(
            self.root,
            height=9,
            width=65,
            font=("Consolas", 11)
        )
        self.input_box.pack(padx=20, pady=5)

        self.input_box.bind("<KeyPress>", self.capture_key)

        buttons = ttk.Frame(self.root)
        buttons.pack(pady=15)

        ttk.Button(
            buttons,
            text="START",
            command=self.start_recording
        ).grid(row=0, column=0, padx=10)

        ttk.Button(
            buttons,
            text="STOP",
            command=self.stop_recording
        ).grid(row=0, column=1, padx=10)

        ttk.Button(
            buttons,
            text="CLEAR",
            command=self.clear_input
        ).grid(row=0, column=2, padx=10)

        self.output = tk.Listbox(
            self.root,
            width=75,
            height=8
        )
        self.output.pack(padx=15, pady=5)

    def start_recording(self):
        self.recording = True
        self.status.config(
            text="● RECORDING",
            foreground="green"
        )
        self.output.insert(tk.END, "Recording dimulai.")

    def stop_recording(self):
        self.recording = False
        self.status.config(
            text="● STOPPED",
            foreground="red"
        )
        self.output.insert(tk.END, "Recording dihentikan.")

    def capture_key(self, event):
        if not self.recording:
            return

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # Abaikan tombol kontrol yang bukan karakter teks.
        if len(event.char) != 1 or not event.char.isprintable():
            return

        with open(
            LOG_FILE,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, event.char])

        self.output.insert(
            tk.END,
            f"{timestamp} | {event.char!r}"
        )
        self.output.see(tk.END)

    def clear_input(self):
        self.input_box.delete("1.0", tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerLab(root)
    root.mainloop()
