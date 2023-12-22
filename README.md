![SlingRING_banner02](https://github.com/Blizaine/SlingRING/assets/7264631/ebeffca7-03e4-4b13-a19c-c1ceab93330c)

# SlingRING

Welcome to SlingRING - an innovative, open-source web application designed to streamline and simplify controlling and accessing various AI applications on your local system. Get ready to "Sling" a portal to all your locally-hosted AI Web-App UIs, from anywhere, via a "Remote Intelligent Neural Gateway." 

## Release Notes:

- **Dec 22nd 2023:** Added gputil added to _install.bat. Added real-time CPU and GPU monitoring to Gradio UI and added real-time status of the running app, which now syncs between browser sessions, showing the active running app.  
- **Dec 5th 2023:** Fixed Gradio bug and added _install.bat
- **Dec 3rd 2023:** New Theme and updated Read Me
- **Dec 1st 2023:** Initial Release


## Why?

Many open-source AI applications are able to run locally on a machine with a powerful GPU. They often present a Web UI via localhost or give you the option to enable remote access to that single application. What about all the other AI apps? What if you forgot to launch it? What if it has problems and needs reset? Or maybe you're just sitting on the couch or at a family gathering and want to show off some of the fantastic things you can do with these tools. This is why I built this application.  I wanted to be able to launch, stop, reset, and remotely access any of my local AI apps from any device, anywhere.

Please keep in mind that while I tried to make things easy, this App, like other open-source tools, is designed for people who know how to install and configure these tools.  It is not (at this point) going to go out and figure out every app you have installed, automatically know if those apps are configured correctly for remote access, configure them for you, and create a secure public URL with SSO & SSL for you to access. But it will let you drop as many start-up BAT scripts as you want into a folder and present that folder as a list remotely, give you start/stop control of those apps, and even parse the live console view for URLs for you to click. :)

With that said, I hope you find this as valuable and enjoyable as I do. 


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
   git clone https://github.com/Blizaine/SlingRING.git
   ```
2. Navigate to the cloned repository:
   ```sh
   cd SlingRING
   ```
3. ```sh
   Open: _instal.bat (from Explorer)
   ```
5. Custom App BATs:
SlingRING relies on BAT files to launch the various AI apps installed on your system.  Since there is no elegant way to know what apps you have or which ones you want to be able to start/stop/reset/access remotely, BAT files will be used.  There is a directory labeled 'apps' that has example BAT files.  But these are common with many of these open-source projects, to automate the launch of the application with appropriate flags and arguments. If your AI app already has a BAT file that launches it, you can have a second BAT file in the 'apps' directory that simply points to your normal launch bat.


### Usage

1. Run the application:
   ```sh
   python app.py

   or

   Open: _Start.bat (from Explorer)
   ```
2. Open the Gradio web interface as directed in the command line output.

### Configuration

- **Logs Directory:** Automatically created at first run. Contains all log files and console outputs.
- **Process File:** A JSON file storing the state of running processes. Required for process management, specifically, stop & reset. 
- **Settings File:** Manage your internal and external IP settings and port number here.  These have no bearing on SlingRING itself and are only used by the URL generator to provide you with a functional link.


## Precautions

### Remote Access and Security

SlingRING does not inherently provide tunneling, VPN, or remote access capabilities. Instead, it relies on the individual applications' ability to be accessed remotely. Users should be aware that each application integrated with SlingRING might support different methods of remote access. SlingRING attempts to simplify those variables by providing links that that pulled from the console output when the app is launched. Including Gradio public URL links.  

- **Local Network Access:** For functionality of this application, you will have to allow local access to SlingRING's port (7861) OR enable Gradio link share.  For apps that don't have Gradio link share, you will need to set up your machine to allow local network access to the specific port(s) of your AI applications, which is often but not always port 7860. For this reason, I've made the default port of SlingRING 7861, to not conflict.  These ports might need to be configured on your computer's Firewall.
- **VPN for Remote Access:** For remote access, consider using a separate VPN solution. This method ensures a secure connection to SlingRING and your local AI applications from outside your local network.
- **Gradio's Public URL Feature:** Some projects may utilize Gradio's feature to generate a random public URL, which remains active for 72 hours. While this is a convenient option for temporary remote access, users should be cautious about the data exposed through these public URLs.  If this is how your AI app(s) are configured, SlingRING is built to be able to parse that unique URL from the command line and present it as a clickable URL to the user, after launching the AI App. 

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

