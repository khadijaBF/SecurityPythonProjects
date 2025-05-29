import pygetwindow as gw
import win32gui
import time
import ctypes
import requests
import platform
import json

# === CONFIGURATION ===
MONITOR_INTERVAL = 10  # seconds
POST_URL = "https://your-enterprise-server.com/api/activity"  # Replace with your endpoint

def get_active_window_title():
    try:
        window = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(window)
    except Exception as e:
        return f"Error retrieving window: {e}"

def get_username():
    try:
        return ctypes.windll.secur32.GetUserNameExW(3)  # NameDisplay
    except:
        return ctypes.windll.kernel32.GetUserNameW()

def get_system_info():
    return {
        "username": get_username(),
        "hostname": platform.node(),
        "os": platform.system(),
        "os_version": platform.version(),
    }

def send_activity_data(data):
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(POST_URL, data=json.dumps(data), headers=headers)
        return response.status_code == 200
    except Exception as e:
        print(f"Failed to send data: {e}")
        return False

def main():
    print("Monitoring started. Press Ctrl+C to stop.")
    sys_info = get_system_info()

    while True:
        activity_data = sys_info.copy()
        activity_data["active_window"] = get_active_window_title()
        activity_data["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")

        print(activity_data)  # For debugging, remove in production
        send_activity_data(activity_data)

        time.sleep(MONITOR_INTERVAL)

if __name__ == "__main__":
    main()
# This script monitors user activity by tracking the active window title and sending it to a specified server endpoint.
# It runs indefinitely, collecting data at specified intervals. 