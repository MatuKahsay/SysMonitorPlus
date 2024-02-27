# SysMonitorPlus
SysMonitorPlus: Real-time system monitoring &amp; data logging for security, compliance, and performance optimization. Secure, user-friendly, and versatile

Disclaimer

This script is for educational purposes only. Use it responsibly and ethically. Ensure you have permission to run this script on the system, and that its operation complies with all relevant laws and regulations. Unauthorized use of this script against systems without explicit consent is illegal and unethical.
Description

This project is a comprehensive keylogger designed for educational purposes and authorized security testing. It captures keyboard strokes, mouse movements, system information, clipboard contents, screenshots, audio recordings, and webcam images. It features data encryption and secure transmission capabilities.
Features

    Keyboard Logging: Captures all keyboard strokes.
    Mouse Movement Logging: Tracks mouse movements and clicks.
    System Information Gathering: Collects detailed system information.
    Clipboard Logging: Records clipboard contents.
    Screenshot Capturing: Takes screenshots at configured intervals.
    Audio Recording: Records ambient sound through the microphone.
    Webcam Image Capturing: Takes pictures using the system's webcam.
    Data Encryption: Encrypts collected data for security.
    Secure Transmission: Sends encrypted data via Telegram.

Installation

Ensure you have Python 3 installed on your system. This project also requires several third-party libraries. Install them using pip:

bash

pip3 install pynput pyperclip cryptography requests pyautogui psutil numpy scipy opencv-python sounddevice

Usage

    Clone the repository or download the script to your local machine.
    Configure the script settings according to your needs. This includes setting file paths, Telegram API tokens, and encryption keys.
    Run the script:

    python3 keylogger.py

bash


Configuration

    File Paths: Set the file_path variable to specify where logs and data should be saved.
    Telegram Settings: Provide your telegram_token and telegram_chat_id for secure data transmission.
    Encryption Key: The script will generate an encryption key upon the first run or load an existing one from the specified file.

Legal Notice

This tool is provided for educational use only. Using this tool against systems without prior explicit consent is illegal and unethical. It is the end user's responsibility to comply with all applicable local, state, and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this tool.
Contributing

Contributions to this project are welcome. Please ensure that any pull requests or contributions adhere to the ethical use and legal compliance outlined above.
License

MIT License
