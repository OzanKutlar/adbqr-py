# Changelog

## 1.3.0

- Add "adbqr reset" command to disconnect all devices and restart the ADB server.

  Runs `adb disconnect`, `adb kill-server`, and `adb start-server` in sequence, removing the need to open Android Studio to restart the ADB server. Each step reports its status individually, and the server start is always attempted even if an earlier step fails.

## 1.2.0

- Add "adbqr connect" command to connect to already paired devices.
- Add "adbqr manual" command to connect using a pairing code, instead of via QR code.

## 1.1.0

- Use half-blocks for QR instead of octants.

  Octants are only supported by a handful of fonts, and seem to have some pixel alignment issues in some cases.

- Use low error correction for QR code.
- Use shorter IDs for service name and passcode.

## 1.0.0

- Initial release