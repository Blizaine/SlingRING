import os
import gradio as gr
from gradio.mix import Parallel
from gradio.components import Dropdown, Textbox, Button
import subprocess
import psutil
import logging
import json
import time
import threading
import sys
from collections import deque
import re
import GPUtil

# Create 'logs' directory if it doesn't exist
logs_dir = os.path.join(os.getcwd(), 'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# Configs
PROCESSES_FILE = os.path.join(logs_dir, 'running_processes.json')
LOG_FILE = os.path.join(logs_dir, 'app_control.log')
OUTPUT_LOG_FILE = os.path.join(logs_dir, 'output.log')
root_dir = os.getcwd()
BAT_FOLDER = os.path.join(root_dir, "apps")
CHECK_INTERVAL = 10

def get_cpu_usage():
    return f"CPU Usage: {psutil.cpu_percent(interval=1)}%"



import GPUtil

def get_gpu_usage():
    gpus = GPUtil.getGPUs()
    if not gpus:
        return "GPU not detected"

    gpu_info = []
    for gpu in gpus:
        gpu_load = f"GPU Load: {gpu.load*100:.1f}%"
        gpu_memory = f"GPU Mem: {gpu.memoryUsed:.1f}/{gpu.memoryTotal:.1f} MB ({gpu.memoryUtil*100:.1f}%)"
        gpu_info.append(f"{gpu_load}\n{gpu_memory}")

    return '\n'.join(gpu_info)


# Define functions that return new component instances
def get_cpu_usage_output():
    return gr.Textbox(value=get_cpu_usage(), label="CPU Usage", interactive=False)

def get_gpu_usage_output():
    return gr.Textbox(value=get_gpu_usage(), label="GPU Usage", interactive=False)

def delete_log_file(log_file_path):
    if os.path.exists(log_file_path):
        os.remove(log_file_path)
        print(f"Deleted existing log file: {log_file_path}")
    else:
        print(f"No existing log file to delete: {log_file_path}")

delete_log_file(OUTPUT_LOG_FILE)
delete_log_file(PROCESSES_FILE)

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

def load_current_state():
    try:
        with open('app_state.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return default values if there's an error loading the file
        return {"action": "Start", "app_selection": "DefaultApp", "status": "Ready"}

# Shared variables
cpu_usage_data = "CPU Usage: 0%"
gpu_usage_data = "GPU Usage: 0%"

# Background thread function to update shared variables
def update_monitoring():
    global cpu_usage_data, gpu_usage_data
    while True:
        cpu_usage_data = get_cpu_usage()
        gpu_usage_data = get_gpu_usage()
        time.sleep(5)  # Update every 5 seconds

monitoring_thread = threading.Thread(target=update_monitoring, daemon=True)
monitoring_thread.start()



def fetch_latest_monitoring_data():
    global cpu_usage_data, gpu_usage_data
    cpu_usage_data = get_cpu_usage()  # Fetch the latest CPU usage
    gpu_usage_data = get_gpu_usage()  # Fetch the latest GPU usage

    # Check if the GPU data contains the expected separator
    if " | " in gpu_usage_data:
        gpu_usage, gpu_temp = gpu_usage_data.split(" | ")
    else:
        # Handle the case where the separator is not present
        gpu_usage = gpu_usage_data
        gpu_temp = ""

    return f"{cpu_usage_data}\n{gpu_usage}\n{gpu_temp}"


# Gradio function to update UI
def get_monitoring_data():
    return cpu_usage_data, gpu_usage_data



class Logger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "a")
        self.fileno = self.log.fileno()

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

    def isatty(self):
        return False

sys.stdout = Logger(OUTPUT_LOG_FILE)

def read_logs(max_lines=100):
    log_lines = deque(maxlen=max_lines)
    with open(OUTPUT_LOG_FILE, "r") as f:
        for line in f:
            log_lines.append(line)
    return ''.join(log_lines)

last_launched_app = ""

# def load_processes():
#     try:
#         with open(PROCESSES_FILE) as f:
#             return json.load(f)
#     except:
#         return {}

def load_processes():
    if not os.path.exists(PROCESSES_FILE):
        with open(PROCESSES_FILE, 'w') as f:
            json.dump({}, f)
        return {}

    try:
        with open(PROCESSES_FILE) as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading processes: {e}")
        return {}

def generate_status_message():
    processes = load_processes()
    if not processes:
        return "No running processes"
    return ', '.join([f"{app}: Running" for app in processes.keys()])



def save_processes(data):
    with open(PROCESSES_FILE, 'w') as f:
        json.dump(data, f)

apps = {}
for bat_file in os.listdir(BAT_FOLDER):
    if bat_file.endswith('.bat'):
        name = os.path.splitext(bat_file)[0]
        apps[name] = {
            "path": os.path.join(BAT_FOLDER, bat_file)
        }

running_processes = load_processes()

def save_state(action, app_selection, status_message):
    state = {
        "action": action,
        "app_selection": app_selection,
        "status": status_message
    }
    state_file_path = os.path.join(logs_dir, 'app_state.json')
    with open(state_file_path, 'w') as file:
        json.dump(state, file)

def load_state():
    # default_state = {"action": "", "app_selection": "", "status": ""}
    state_file_path = os.path.join(logs_dir, 'app_state.json')
    try:
        with open(state_file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        with open(state_file_path, 'w') as file:
            json.dump(default_state, file)
        return default_state

initial_state = load_state()
lock = threading.Lock()
    
def control_app(action, app_selection):
    global last_launched_app, running_processes  # Declare global variables

    logging.info(f"Received action: {action} for app: {app_selection}")
    status_message = ""

    if app_selection in apps:
        app_path = apps[app_selection]["path"]

    if action == "Start":
        # ... Existing code for starting the app ...
        with open(OUTPUT_LOG_FILE, "w") as f:
            pass

        last_launched_app = app_selection
        log_fd = sys.stdout.fileno
        
        env = os.environ.copy()
        env['PYTHONUNBUFFERED'] = '1'

        process = subprocess.Popen([app_path], stdout=log_fd, stderr=log_fd, shell=True, env=env)
        running_processes[app_selection] = process.pid
        save_processes(running_processes)  # Save the updated processes
        status_message = generate_status_message() 

    elif action == "Stop":
        # ... Existing code for stopping the app ...
        with open(OUTPUT_LOG_FILE, "w") as f:
            pass
        if app_selection in running_processes:
            # ... Existing code for stopping the process ...
            pid = running_processes[app_selection]
            process = psutil.Process(pid)
            for child in process.children(recursive=True):
                child.terminate()
            process.terminate()
            process.wait()
            del running_processes[app_selection]
            save_processes(running_processes)  # Save the updated processes
            status_message = generate_status_message() 

    else:
        status_message = "Action not recognized"

    # Generate and return the status message
    running_processes = load_processes()  # Reload the processes
    status_message = generate_status_message()  # Generate a new status message
    save_state(action, app_selection, status_message)  # Save the current state
    return status_message

    

def get_app_url(_, app_selection):
    try:
        with open(SETTINGS_FILE) as file:
            settings = json.load(file)
            url = f"http://{settings['internal_ip']}:{settings['port']}/..."
            # Construct the URL using internal_ip and port
            return f"<a href='{url}' target='_blank'>{url}</a>"
    except FileNotFoundError:
        return "Settings not configured"




def extract_urls_from_log(log_file_path):
    url_pattern = re.compile(r'http[s]?://[^\s]+')
    gradio_urls = []
    ip_urls = []

    try:
        with open(SETTINGS_FILE) as file:
            settings = json.load(file)
            internal_ip = settings['internal_ip']
    except FileNotFoundError:
        internal_ip = "0.0.0.0"

    with open(log_file_path, 'r') as file:
        for line in file:
            matches = url_pattern.findall(line)
            for match in matches:
                # Replace "0.0.0.0" with internal IP
                match = match.replace("0.0.0.0", internal_ip)
                if "gradio.live" in match:
                    gradio_urls.append(match)
                elif re.match(r'http[s]?://\d+\.\d+\.\d+\.\d+', match):  # Matches numerical IP addresses
                    ip_urls.append(match)

    # Concatenate lists with gradio URLs at the top, followed by IP URLs
    sorted_urls = gradio_urls + ip_urls

    # Convert URLs to HTML anchor tags
    sorted_urls = [f"<a href='{url}' target='_blank'>{url}</a>" for url in sorted_urls]

    return sorted_urls


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

html = '''
<head> <link rel="apple-touch-icon" href="SlingRING2.png"> </head>
'''
# Define a function to fetch the latest status
def fetch_latest_status():
    return generate_status_message()

my_theme = gr.Theme.from_hub("ParityError/Interstellar")

# Blocks interface
with gr.Blocks(title = "SlingRING", theme=my_theme) as app:
    gr.Markdown(
    """
    # SlingRING
    """)
    with gr.Tab("Control"):
        with gr.Row():
            action_dropdown = gr.Dropdown(choices=["Start", "Stop"], label="Action", value=initial_state['action'], allow_custom_value=False, interactive=True)  # Default to "Start"
            app_dropdown = gr.Dropdown(choices=list(apps.keys()), label="App Selection", value=initial_state['app_selection'], allow_custom_value=False, interactive=True)  # Default to "DefaultApp"
            # status_output = gr.Textbox(label="Status", value=initial_state['status'], interactive=False)  # Default status message
            status_output = gr.Textbox(label="Status", value=generate_status_message(), interactive=False)
            cpu_usage_output = gr.Textbox(label="CPU/GPU Usage", interactive=False)
            app.load(fetch_latest_monitoring_data, None, cpu_usage_output, every=3)
            app.load(fetch_latest_status, None, status_output, every=3) 


            submit_button = Button("Submit")
        logs = gr.Textbox(label="Live Console View")
        app.load(read_logs, None, logs, every=3)

        url_output = gr.HTML()
        url_button = gr.Button("Refresh URLs")
        url_button.click(fn=display_urls, outputs=url_output)

        submit_button.click(
            fn=control_app,
            inputs=[action_dropdown, app_dropdown],
            outputs=status_output  # This should update the status textbox
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
# Custom JavaScript for periodic polling
javascript = """
setInterval(function() {
    document.querySelector('button[data-testid="Fetch Data"]').click();
}, 5000);  // 5000 milliseconds = 5 seconds
"""

# Background process to periodically save
def background_process():
    while True:
        save_processes(running_processes)  
        time.sleep(CHECK_INTERVAL)
        
bg_process = threading.Thread(target=background_process)
bg_process.start()


app.queue().launch(inbrowser=True, server_name="0.0.0.0", server_port=7861, favicon_path="SlingRING2.png")
app.launch(inline_js=javascript)