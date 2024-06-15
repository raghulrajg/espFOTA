# OTAUpdateManager
espFOTA: An OTA (Over-the-Air) update library for ESP8266, ESP32, and other devices supporting MicroPython.

[![micropython](https://img.shields.io/badge/micropython-Ok-purple.svg)](https://micropython.org)

[![ESP8266](https://img.shields.io/badge/ESP-8266-000000.svg?longCache=true&style=flat&colorA=CC101F)](https://www.espressif.com/en/products/socs/esp8266)

[![ESP32](https://img.shields.io/badge/ESP-32-000000.svg?longCache=true&style=flat&colorA=CC101F)](https://www.espressif.com/en/products/socs/esp32)
[![ESP32](https://img.shields.io/badge/ESP-32S2-000000.svg?longCache=true&style=flat&colorA=CC101F)](https://www.espressif.com/en/products/socs/esp32-s2)
[![ESP32](https://img.shields.io/badge/ESP-32C3-000000.svg?longCache=true&style=flat&colorA=CC101F)](https://www.espressif.com/en/products/socs/esp32-c3)


# espFOTA

**espFOTA** is an Over-the-Air (OTA) update library for MicroPython devices such as ESP8266, ESP32, and other supported hardware. This library simplifies the process of updating firmware over a Wi-Fi connection, ensuring your devices are always up-to-date.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Setup](#setup)
  - [Network Status Indicator](#network-status-indicator)
  - [Automatic Update Check](#automatic-update-check)
- [Example Node.js Server](#example-nodejs-server)
- [Important Notes](#important-notes)

## Features

- Easy configuration for OTA updates.
- Automatic Wi-Fi connection management.
- Continuous update checks with automatic application of updates.
- Network status indicator using GPIO pin.

## Installation

### Installing with mip

Py-file
```python
import mip
mip.install('github:raghulrajg/espFOTA/espFOTA.py')
```

To install using mpremote

```bash
    mpremote mip install github:raghulrajg/espFOTA
```

To install directly using a WIFI capable board

```bash
    mip.install("github:raghulrajg/espFOTA")
```

### Installing Library Examples

If you want to install library examples:

```bash
    mpremote mip install github:raghulrajg/espFOTA/examples.json
```

To install directly using a WIFI capable board

```bash
    mip.install("github:raghulrajg/espFOTA/examples.json")
```

### Installing from PyPI

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/micropython-espFOTA/>`_.
To install for current user:

```bash
    pip3 install micropython-espFOTA
```

To install system-wide (this may be required in some cases):


```bash
sudo pip3 install micropython-espFOTA
```
To install in a virtual environment in your current project:

```bash
    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .env/bin/activate
    pip3 install micropython-espFOTA
```

Also see [examples](https://github.com/raghulrajg/espFOTA/tree/main/test).

## Usage

### Setup

1. **Wi-Fi and Server Configuration:**
    - `SSID`: Your Wi-Fi network name.
    - `Password`: Your Wi-Fi network password.
    - `host`: The server endpoint where the update file is hosted.

2. **Example Program:**

    Save the following code in a file named `main.py` on your MicroPython device:

    ```python
    import espFOTA

    # Avoid the GPIO pin number 2 because of predefine pin (Network status indicator)

    # Server connection config
    host = "package.xyz.com/newversion"

    # WiFi Network connection config
    SSID = "YOUR_APN_NAME"
    Password = "YOUR_APN_PASSWORD"

    OTAUpdate = espFOTA.espFOTA(SSID, Password, host)

    def loop():
        while True:
            # Put your code here
            OTAUpdate.run()

    if __name__ == '__main__':
        loop()
    ```

    - **SSID**: Replace with your Wi-Fi network name.
    - **Password**: Replace with your Wi-Fi network password.
    - **host**: Replace with your server's URL endpoint where the OTA update file is hosted.

### Network Status Indicator

- The device uses GPIO pin 2 as a network status indicator.
- If the Wi-Fi network is not connected, the LED on GPIO pin 2 will turn on.
- Once the Wi-Fi is connected, the LED will turn off.

### Automatic Update Check

- The `OTAUpdate.run()` method continuously checks for updates from the specified host.
- If an update is found, it is automatically downloaded and applied.
- The device will restart to apply the new firmware.

## Example Node.js Server

To serve the OTA update file, you can set up a simple Node.js server. Here is an example:

```javascript
const http = require('http');
const url1 = require('url');
const fs = require('fs');

const server1 = http.createServer((req, res) => {
  const parsedUrl = url1.parse(req.url, true);
  const pathname = parsedUrl.pathname;
  if (pathname === '/download') {
    const filePath = `filepath/ota.py`;  // Path to your OTA update file

    // Send the bin file to esp32
    serveFile(res, filePath);
  } else {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('Not found');
  }
});

function serveFile(res, filePath) {
  const stat = fs.statSync(filePath);
  const fileStream = fs.createReadStream(filePath);
  res.writeHead(200, {
    'Content-Type': 'application/octet-stream',
    'Content-Length': stat.size,
    'Content-Disposition': 'attachment; filename=' + "ota.py"
  });
  console.log(stat.size);
  fileStream.pipe(res);
  console.log("Downloaded");
  fs.unlinkSync(filePath); 
}

server1.listen(3000, () => {
  console.log('Server listening on port 3000');
});
```
### Server Setup:

- Save the above code in a file, e.g., `server.js`.
- Ensure you have Node.js installed.
- Run the server using the command: node `server.js`.

### Endpoint: 

- The server listens on port 3000. The OTA update file should be accessible at `http://<server-ip>:3000/download`.

## Important Notes

- File Naming: The example program file name must be `main.py` on your MicroPython device.
- Wi-Fi and Host Configuration: Ensure that the SSID, Password, and host variables are correctly set to match your network and server configurations.
- Update Check Frequency: The `OTAUpdate.run()` method continuously checks for updates. Adjust the frequency or conditions within the loop function as needed.

