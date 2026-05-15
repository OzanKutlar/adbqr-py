import qrcode

class QrRenderer:
    def __init__(self, data: str):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=1,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        self.matrix = qr.modules
        self.width = len(self.matrix[0])
        self.height = len(self.matrix)

    def render(self):
        print()
        for y in range(self.height):
            row = "  " # Left indent for visual padding
            for x in range(self.width):
                if self.matrix[y][x]:
                    # Black background, two spaces wide for square aspect ratio
                    row += "\x1b[40m  "
                else:
                    # White background, two spaces wide
                    row += "\x1b[47m  "
            row += "\x1b[0m" # Reset color at end of line
            print(row)
        print()
