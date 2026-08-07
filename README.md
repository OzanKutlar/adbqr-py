# adbqr (Python)

adbqr is a simple command line tool to manage wireless ADB connections easily, like in Android Studio.

This is a Python fork/port of the original Rust project: [soxfox42/adbqr](https://github.com/soxfox42/adbqr). It provides seamless installation and dependency management for Python users.

## Why use this?

Connecting your device via wireless ADB can be tedious if you are not using Android Studio. For instance, when using wireless connections for non-development actions like mirroring with [scrcpy](https://github.com/genymobile/scrcpy), you normally have to manually look up and type your phone's IP address and port to pair and connect.

Although modern Android devices natively support QR code pairing, the standard `adb` CLI tool has no built-in way to generate or display these QR codes.

**adbqr** solves this by:
- **Printing a pairing QR code** directly in your terminal, which you can scan with your phone to pair and connect instantly.
- **Auto-discovering devices** on your local network that have "Pair device with pairing code" enabled, mimicking Android Studio's seamless discovery so you don't have to manually type in IP addresses or ports.

## Installation

Requires Python 3.10+.

First, clone this repository and navigate into the directory:

```bash
git clone https://github.com/OzanKutlar/adbqr-py.git
cd adbqr-py
pip install .
# or for development:
pip install -e .
```

During your first run, the CLI will automatically detect the `adb` executable in your `PATH` or current directory. If it isn't found, you will be prompted to provide the full path to `adb`.

## Usage

After installation, the `adbqr` command is available in your terminal. 

```bash
# Default command: initiates QR code pairing.
adbqr 

# Explicitly initiate QR code pairing.
adbqr pair

# Initiate manual pairing via pairing code.
# This is still faster than a regular `adb pair` command as the tool automatically 
# detects phones on the network that have entered into "pair with code" mode.
adbqr manual
# Connect to an already paired device on the network.
adbqr connect

# Disconnect all devices and restart the ADB server.
# Use this when ADB gets into a bad state (stale "offline" devices,
# connections that refuse to establish) instead of reaching for
# Android Studio's "Restart ADB server" button.
adbqr reset
```

> [!WARNING]
> `adbqr reset` restarts the ADB daemon, which drops **every** active connection, including USB-attached devices and any running `scrcpy` session.

**Pairing Instructions:**
Make sure your Android device is on the same network as your computer.
1. On your Android device, open **Developer options**.
2. Open **Wireless debugging**, and enable it if necessary.
3. Select the respective pairing option based on your command (QR code or pairing code).
4. Follow the on-screen terminal instructions.

## Screenshots

### Screenshot of QR mode

![adbqr QR Mode Screenshot](screenshot_qr.png)

<br>

### Screenshot of manual mode

![adbqr Manual Mode Screenshot](screenshot_manual.png)
