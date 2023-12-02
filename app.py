import os
import gradio as gr  
from gradio.mix import Parallel
from gradio.components import Dropdown, Textbox, Button
import subprocess
import psutil
import logging
import webbrowser
import json
import time
import threading
import sys
from collections import deque
import re
import os


# Create 'logs' directory if it doesn't exist
logs_dir = os.path.join(os.getcwd(), 'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# Configs
PROCESSES_FILE = os.path.join(logs_dir, 'running_processes.json') 
LOG_FILE = os.path.join(logs_dir, 'app_control.log')
OUTPUT_LOG_FILE = os.path.join(logs_dir, 'output.log')
root_dir = os.getcwd()  # Gets the current working directory (root of the app)
BAT_FOLDER = os.path.join(root_dir, "apps")
CHECK_INTERVAL = 10 # seconds

def delete_log_file(log_file_path):
    if os.path.exists(log_file_path):
        os.remove(log_file_path)
        print(f"Deleted existing log file: {log_file_path}")
    else:
        print(f"No existing log file to delete: {log_file_path}")

# Call the function to delete the output.log file
delete_log_file(OUTPUT_LOG_FILE)


# Logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

class Logger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "a")  # Use append mode
        self.fileno = self.log.fileno()  # File descriptor for the log file

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        
    def flush(self):
        self.terminal.flush()
        self.log.flush()
        
    def isatty(self):
        return False      

sys.stdout = Logger(OUTPUT_LOG_FILE)

def test(x):
    print("This is a test")
    print(f"Your function is running with input {x}...")
    return x

def read_logs(max_lines=100):
    log_lines = deque(maxlen=max_lines)
    with open(OUTPUT_LOG_FILE, "r") as f:
        for line in f:
            log_lines.append(line)
    return ''.join(log_lines)

# Define last_launched_app globally
last_launched_app = None

def load_processes():
    try:
        with open(PROCESSES_FILE) as f:
            return json.load(f)
    except:  
        return {}

def save_processes(data):
    with open(PROCESSES_FILE, 'w') as f: 
        json.dump(data, f)
        
# Get available apps
apps = {}
for bat_file in os.listdir(BAT_FOLDER):
    if bat_file.endswith('.bat'):
        name = os.path.splitext(bat_file)[0]
        apps[name] = {
            "path": os.path.join(BAT_FOLDER, bat_file) 
        }
    
# Track processes
running_processes = load_processes()

# Function to control the app
def control_app(action, app_selection):
    global last_launched_app
    logging.info(f"Received action: {action} for app: {app_selection}")

    if app_selection in apps:
        app_path = apps[app_selection]["path"]

    if action == "Launch":
        with open(OUTPUT_LOG_FILE, "w") as f:
            pass  # Opening in write mode with no content will clear the file

        last_launched_app = app_selection
        log_fd = sys.stdout.fileno  # Get file descriptor of the logger
        
        env = os.environ.copy()
        env['PYTHONUNBUFFERED'] = '1'

        # process = subprocess.Popen([app_path], stdout=log_fd, stderr=log_fd, shell=True, env=os.environ)
        process = subprocess.Popen([app_path], stdout=log_fd, stderr=log_fd, shell=True, env=env)
        running_processes[app_selection] = process.pid

        running_processes[app_selection] = process.pid
        logging.info(f"Launched {app_selection}")
        return f"Action performed: {action} on {app_selection}"

    elif action == "Stop":
        with open(OUTPUT_LOG_FILE, "w") as f:
            pass  # Opening in write mode with no content will clear the file
        if app_selection in running_processes:
            try:
                pid = running_processes[app_selection]
                process = psutil.Process(pid)
                # Terminate child processes
                for child in process.children(recursive=True):
                    child.terminate()
                process.terminate()
                process.wait()  # Wait for the process to terminate
                del running_processes[app_selection]
                logging.info(f"Successfully stopped {app_selection}")
                if last_launched_app == app_selection:
                        last_launched_app = None
            except Exception as e:
                logging.error(f"Error stopping {app_selection}: {e}")
            return f"Stopped {app_selection}"
        else:
            logging.warning(f"Attempted to stop non-running app: {app_selection}")
            return "App not running or not found"
            return f"Action performed: {action} on {app_selection}"
        

    # elif action == "Reset":
    #     with open(OUTPUT_LOG_FILE, "w") as f:
    #         pass  # Opening in write mode with no content will clear the file
    #     if app_selection in running_processes:
    #         try:
    #             process = running_processes[app_selection]
    #             # Terminate child processes
    #             parent = psutil.Process(process.pid)
    #             for child in parent.children(recursive=True):
    #                 child.terminate()
    #             parent.terminate()
    #             parent.wait()  # Wait for the process to terminate
    #             del running_processes[app_selection]
    #             # Relaunch the app
    #             process = subprocess.Popen([app_path] + args.split())
    #             running_processes[app_selection] = process
    #             logging.info(f"Reset {app_selection}")
    #         except Exception as e:
    #             logging.error(f"Error resetting {app_selection}: {e}")
    #         return f"Reset {app_selection}"
    #     else:
    #         logging.warning(f"Attempted to reset non-running app: {app_selection}")
    #         return "App not running or not found"

    # else:
    #     logging.error(f"Invalid action: {action}")
    #     return "Invalid action"


def get_app_url(_, app_selection):
    try:
        with open(SETTINGS_FILE) as file:
            settings = json.load(file)
            url = f"http://{settings['internal_ip']}:{settings['port']}/..."
            # Construct the URL using internal_ip and port
            return f"<a href='{url}' target='_blank'>{url}</a>"
    except FileNotFoundError:
        return "Settings not configured"


# Function to extract URL from log file
def extract_urls_from_log(log_file_path):
    url_pattern = re.compile(r'http[s]?://[^\s]+')
    urls = []

    # Read the internal IP from settings
    try:
        with open(SETTINGS_FILE) as file:
            settings = json.load(file)
            internal_ip = settings['internal_ip']
    except FileNotFoundError:
        internal_ip = "0.0.0.0"  # Default value if settings are not found

    with open(log_file_path, 'r') as file:
        for line in file:
            matches = url_pattern.findall(line)
            for match in matches:
                if "0.0.0.0" in match:
                    match = match.replace("0.0.0.0", internal_ip)
                urls.append(f"<a href='{match}' target='_blank'>{match}</a>")
    return urls


SETTINGS_FILE = os.path.join(logs_dir, 'settings.json')

def save_settings(internal_ip, external_ip, port):
    settings = {
        "internal_ip": internal_ip,
        "external_ip": external_ip,
        "port": int(port)  # Convert port to integer
    }
    with open(SETTINGS_FILE, 'w') as file:
        json.dump(settings, file)



# Shared variable to store the latest URL
latest_urls = []

# Background function to update the URL list
def update_url():
    global latest_urls
    while True:
        latest_urls = extract_urls_from_log(OUTPUT_LOG_FILE)
        time.sleep(5)  # Check every 5 seconds

# Gradio function to display the URL list
def display_urls():
    # Extract URLs from the log file
    log_urls = extract_urls_from_log(OUTPUT_LOG_FILE)
    labeled_urls = [f"URL from Console: {url}" for url in log_urls]  # Label each log URL

    # Read saved settings and construct new URLs with labels
    try:
        with open(SETTINGS_FILE) as file:
            settings = json.load(file)
            internal_url = f"http://{settings['internal_ip']}:{settings['port']}"
            external_url = f"http://{settings['external_ip']}:{settings['port']}"

            internal_url_labeled = f"Internal URL: <a href='{internal_url}' target='_blank'>{internal_url}</a>"
            external_url_labeled = f"External URL: <a href='{external_url}' target='_blank'>{external_url}</a>"

            labeled_urls.extend([internal_url_labeled, external_url_labeled])  # Append the labeled custom URLs
    except FileNotFoundError:
        # If settings are not found, we don't add the custom URLs
        pass

    return '<br>'.join(labeled_urls)  # Join all URLs with labels and line breaks

# Start the background thread
threading.Thread(target=update_url, daemon=True).start()

def load_settings():
    try:
        with open(SETTINGS_FILE) as file:
            return json.load(file)
    except FileNotFoundError:
        return {"internal_ip": "", "external_ip": "", "port": ""}

saved_settings = load_settings()

# javascript = """
# function addAppleTouchIcon() {
#     var link = document.createElement('link');
#     link.rel = 'apple-touch-icon';
#     link.sizes = '180x180';
#     link.href = 'webui/SlingRING2.png';
#     document.head.appendChild(link);
# }
# addAppleTouchIcon();
# """
# 
# 
# theme = gr.themes.Soft(primary_hue="slate")

my_theme = gr.Theme.from_hub("ParityError/Interstellar")

# Blocks interface
with gr.Blocks(title = "SlingRING", theme=my_theme) as app:
    gr.Markdown(
    """
    # SlingRING
    """)
    with gr.Tab("Control"):
        with gr.Row():
            # action_dropdown = Dropdown(choices=["Launch", "Stop", "Reset"], label="Action")
            action_dropdown = Dropdown(choices=["Launch", "Stop"], label="Action")
            app_dropdown = Dropdown(choices=list(apps.keys()), label="App Selection")
            submit_button = Button("Submit")

        status_output = Textbox(label="Status", interactive=False)
        
        logs = gr.Textbox(label="Live Console View")
        app.load(read_logs, None, logs, every=3)

        url_output = gr.HTML()
        url_button = gr.Button("Refresh URLs")
        url_button.click(fn=display_urls, outputs=url_output)

        submit_button.click(
            fn=control_app, 
            inputs=[action_dropdown, app_dropdown], 
            outputs=[status_output]
        )
    with gr.Tab("Settings"):
        with gr.Column():
            internal_ip_input = gr.Textbox(label="Internal IP Address", value=saved_settings["internal_ip"])
            external_ip_input = gr.Textbox(label="External IP Address", value=saved_settings["external_ip"])
            port_input = gr.Number(label="Port Number", value=saved_settings["port"])
            save_settings_button = gr.Button("Save Settings")
    save_settings_button.click(
        fn=save_settings,
        inputs=[internal_ip_input, external_ip_input, port_input],
        outputs=[], 
    )

# Background process to periodically save
def background_process():
    while True:
        save_processes(running_processes)  
        time.sleep(CHECK_INTERVAL)
        
bg_process = threading.Thread(target=background_process)
bg_process.start()

app.queue().launch(inbrowser=True, share=True, server_name="0.0.0.0", server_port=7861, favicon_path="SlingRING2.png")
