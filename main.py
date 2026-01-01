import subprocess
import sys
import os
import pyttsx3
import tkinter as tk
from tkinter import messagebox
from PIL import ImageGrab, Image
import pytesseract
import threading
import time

# Function to auto-install packages
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Try to import and install if missing
try:
    import pytesseract
except:
    install('pytesseract')
    import pytesseract

try:
    from PIL import ImageGrab, ImageTk, Image
except:
    install('Pillow')
    from PIL import ImageGrab, ImageTk, Image

try:
    import pyttsx3
except:
    install('pyttsx3')
    import pyttsx3

try:
    import tkinter as tk
    from tkinter import messagebox
except:
    install('tk')
    import tkinter as tk
    from tkinter import messagebox

# Set up Tesseract path if needed (adjust based on OS)
if os.name == 'nt':  # Windows
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

engine = pyttsx3.init()
voices = engine.getProperty('voices')
current_voice = 0

# Screen Reader GUI
class ScreenReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Reader")
        self.root.configure(bg='#0a0a0a')
        self.root.geometry('350x500+100+100')  # Set window size and fixed position
        self.root.attributes('-topmost', True)  # Keep window always on top
        self.root.resizable(False, False)       # Disable resizing
        # self.root.overrideredirect(True)      # Uncomment to remove title bar (optional)

        self.create_widgets()

    def create_widgets(self):
        # Title Label
        self.title = tk.Label(self.root, text="SCREEN READER", font=("Orbitron", 16),
                              fg="#c0aaff", bg="#0a0a0a")
        self.title.pack(pady=20)

        # Live Reading Button
        self.read_button = tk.Button(self.root, text="LIVE READING", command=self.start_live_reading,
                                     font=("Orbitron", 12), bg="#111", fg="#00f0ff", bd=2,
                                     relief="solid", highlightbackground="#00f0ff",
                                     activebackground="#00f0ff", activeforeground="#000")
        self.read_button.pack(pady=10, ipadx=10, ipady=5)

        # Select Area Button
        self.select_button = tk.Button(self.root, text="SELECT AREA", command=self.select_area,
                                       font=("Orbitron", 12), bg="#111", fg="#00f0ff", bd=2,
                                       relief="solid", highlightbackground="#00f0ff",
                                       activebackground="#00f0ff", activeforeground="#000")
        self.select_button.pack(pady=10, ipadx=10, ipady=5)

        # Output Text Area
        self.output = tk.Text(self.root, height=6, width=35, bg="#111", fg="#aaa", bd=0,
                              wrap=tk.WORD, font=("Arial", 10))
        self.output.pack(pady=15)

        # Switch Voice Button
        self.voice_button = tk.Button(self.root, text="SWITCH VOICE", command=self.switch_voice,
                                      font=("Orbitron", 12), bg="#111", fg="#00f0ff", bd=2,
                                      relief="solid", highlightbackground="#00f0ff",
                                      activebackground="#00f0ff", activeforeground="#000")
        self.voice_button.pack(pady=10, ipadx=10, ipady=5)

        # Creator Label
        self.creator_label = tk.Label(self.root, text="Created by K R Hari Prajwal", font=("Arial", 8),
                                      fg="#777", bg="#0a0a0a")
        self.creator_label.pack(side=tk.BOTTOM, pady=5)

    def start_live_reading(self):
        # Start live reading in a separate thread so that the UI remains responsive
        threading.Thread(target=self.live_reading).start()

    def live_reading(self):
        try:
            while True:
                img = ImageGrab.grabclipboard()  # Use clipboard as source
                if img:
                    text = pytesseract.image_to_string(img)
                    self.output.delete('1.0', tk.END)
                    self.output.insert(tk.END, text.strip())
                    engine.say(text)
                    engine.runAndWait()
                time.sleep(1)
        except Exception as e:
            messagebox.showerror("Error", f"Live reading failed: {e}")

    def select_area(self):
        messagebox.showinfo("Instruction", "Press PrtSc (Print Screen) and Ctrl+C to copy to clipboard, then click 'LIVE READING'.")

    def switch_voice(self):
        global current_voice
        current_voice = (current_voice + 1) % len(voices)
        engine.setProperty('voice', voices[current_voice].id)
        engine.say("Voice switched")
        engine.runAndWait()

# Main entry
if __name__ == '__main__':
    root = tk.Tk()
    app = ScreenReaderApp(root)
    root.mainloop()
