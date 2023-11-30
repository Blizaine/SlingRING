
# SlingRING

Welcome to SlingRING - an innovative, open-source web application designed to streamline and simplify the process of controlling and accessing various AI applications on your local system. There are so many great open-source AI applications that will run locally, on a machine with a powerful GPU, but they often only present the user with access via a localhost web UI. And while the Web UI can be configured for remote access, what happens when you want to switch the application that is running on your machine but you are not at home? or maybe just sitting on the couch? This is why I built this application.  I wanted to be able to launch, stop, and reset Automatic1111 from my iPhone. But also be able to access FaceFusion ComfyUI, or Stable Video, when I have an idea pop into my head.  Built with flexibility and efficiency in mind, SlingRING is purpose-built to offer a user-friendly interface for AI apps with management, logging capabilities, and URL handling, all accessible through a simple Gradio web interface.

## Features

- **Process Control:** Launch, stop, and reset your existing AI applications with ease.
- **CMD View:** Real-time remote view of CLI.
- **URL Extraction and Display:** Automatically extract and display clickable URLs from cmd/python outputs.
- **Settings Management:** Configure/Save internal and external IP addresses and port numbers for automatic URL generation.
- **Background Operations:** Update URLs and save process states periodically in the background.
- **User-Friendly Interface:** Manage and monitor processes through an intuitive Gradio web interface.


## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.x

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/[your-username]/SlingRING.git
   ```
2. Navigate to the cloned repository:
   ```sh
   cd SlingRING
   ```
3. Custom App BATs:
   SlingRING relies on BAT files to launch the various AI apps installed on your system.  Since there is no elegant way to know what apps you have or which ones you want to be able to start/stop/reset/access remotely, BAT files will be used.  There is a directory in git labeled 'apps' that has example BAT files.  But these are fairly typical and common with many of these open-source projects to automate the launch of the application with appropriate flags and arguments. this is really hard. 



### Usage

1. Run the application:
   ```sh
   python app.py

   or

   Double Click: Start.bat
   ```
2. Open the Gradio web interface as directed in the command line output.

### Configuration

- **Logs Directory:** Automatically created at first run. Contains all log files.
- **Process File:** A JSON file storing the state of running processes. Required for process management, specifically, stop & reset. 
- **Settings File:** Manage your internal and external IP settings and port number here.  These have no bearing on SlingRING itself and are only used by the URL generator to provide you with a functional link.


## Precautions

### Remote Access and Security

SlingRING does not inherently provide tunneling, VPN, or remote access capabilities. Instead, it relies on the individual applications' ability to be accessed remotely. Users should be aware that each application integrated with SlingRING might support different methods of remote access. SlingRING attempts to bridge the gap that is inherent in having different apps that support different protocols, but it is a work in progress. 

- **Local Network Access:** For based functionality of this application, it's recommended to set up your machine to allow local network access, to your specific port(s) of your AI applications, for safety and control.
- **VPN for Remote Access:** For remote access, consider using a separate VPN solution. This method ensures a secure connection to your applications from outside your local network.
- **Gradio's Public URL Feature:** Some projects may utilize Gradio's feature to generate a random public URL, which remains active for 72 hours. While this is a convenient option for temporary remote access, users should be cautious about the data exposed through these public URLs.  If this is how your AI app(s) are configured, SlingRING is built to be able to parse that unique URL from the command line and present it as a clickable URL to the user. 

### Best Practices for Security

- Always ensure that your network is secured, especially when allowing remote access to applications.
- Regularly update your applications and security measures to protect against vulnerabilities.
- Be aware of the security features and limitations of each application you are managing through SlingRING.

Remember, while SlingRING facilitates the management of applications, it is the user's responsibility to ensure secure and appropriate remote access setups according to their needs and the capabilities of the individual applications.


## Contributing

Contributions are what makes the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Blaine Brown - [@Blizaine](https://twitter.com/blizaine) 

