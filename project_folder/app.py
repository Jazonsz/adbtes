import subprocess
import time
import os
from flask import Flask, render_template, request

# ADB path and emulator ports
adb = r'"C:\\Program Files\\Netease\\MuMuPlayerGlobal-12.0\\shell\\adb.exe"'
ports = {"jason": "16384", "sendy": "16416"}
screenshot_dir = 'static/screenshots'

# Create directory for screenshots if it doesn't exist
os.makedirs(screenshot_dir, exist_ok=True)

app = Flask(__name__)

# Functions to interact with emulators
def connect_to_emulators():
    for port in ports.values():
        subprocess.run(f'{adb} connect 127.0.0.1:{port}', shell=True)

def list_adb():
    r = subprocess.run(f'{adb} devices', capture_output=True, text=True, shell=True)
    return [line.split('\t')[0] for line in r.stdout.strip().split('\n')[1:]]

def take_screenshot(instance, filename):
    subprocess.run(f'{adb} -s {instance} exec-out screencap -p > {filename}', shell=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    screenshot_file = None
    if request.method == 'POST':
        alias = request.form.get('alias')
        if alias in ports:
            port = ports[alias]
            instance = f"127.0.0.1:{port}"
            if instance in list_adb():
                screenshot_file = f"screenshot_{port}.png"
                screenshot_path = os.path.join(screenshot_dir, screenshot_file)
                take_screenshot(instance, screenshot_path)
                screenshot_file = f'screenshots/{screenshot_file}'  # Correct relative path for rendering in HTML
    
    return render_template('index.html', ports=ports, screenshot_file=screenshot_file)

# Connect to emulators initially
connect_to_emulators()

if __name__ == "__main__":
    app.run(debug=True)
