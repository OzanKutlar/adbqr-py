# adbqr

[![Crates.io Version](https://img.shields.io/crates/v/adbqr)](https://crates.io/crates/adbqr)

adbqr is a simple command line tool to manage wireless ADB connections easily, like in Android Studio.
It has been recently ported to Python for seamless installation and dependency management.

## Installation

Requires Python 3.10+.

```bash
pip install .
# or for development:
pip install -e .
```

During your first run, the CLI will automatically detect the `adb` executable in your `PATH` or current directory. If it isn't found, you will be prompted to provide the full path to `adb`.

## Screenshots

![adbqr QR Mode Screenshot](screenshot_qr.png)
![adbqr Manual Mode Screenshot](screenshot_manual.png)
