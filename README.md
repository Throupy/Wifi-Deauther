# Wifi-Deauther

This tool is for testing and education purposes only 
<b>Do not use this tool against any Wi-Fi networks that you do not have permission to test</b>
<hr>
### Overview
This tool provides a web interface which shows the user all of the access points within range, and gives an option to "Jam" them. The jamming is done by sending de-authentication frames to all devices (broadcast) on the network. The result will be all devices being disconnected from the target Wi-Fi network.

The program is designed to run on a Raspberry Pi with a touchscreen, below is the hardware that the program has been tested on.
- Raspberry Pi Model 3b+
- Official Raspberry Pi 7" Touchscreen
- External USB Wi-Fi interface with MT7601u chipset
- A 3D printed case for the device (coming soon, images to follow)

### Usage
First the web server must be started. If the user is only using the touch screen, a bash script could be made to automate this.
```bash
sudo python app.py
```
Next navigate to the webserver at
```bash
chromium-browser http://localhost:8000/ --start-fullscreen
```
Below is a list of the third-party libraries used:
- Flask
- Scapy

### Future Updates
- Give the user a choice to disconnect a certain device from a network
- Improve the web interface, maybe even convert to a native GUI application
- Upload photos of the device (waiting for case)