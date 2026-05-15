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
        for y in range(0, self.height, 2):
            # \x1b[30;47m forces black foreground (30) and white background (47)
            row = "\x1b[30;47m"
            for x in range(self.width):
                top_dark = self.color(x, y)
                bottom_dark = self.color(x, y + 1)

                if not top_dark and not bottom_dark:
                    row += ' '
                elif not top_dark and bottom_dark:
                    row += '▄'
                elif top_dark and not bottom_dark:
                    row += '▀'
                elif top_dark and bottom_dark:
                    row += '█'
            # Reset colors at the end of the line so it doesn't bleed
            row += "\x1b[0m"
            print(row)

    def color(self, x: int, y: int) -> bool:
        if x >= self.width or y >= self.height:
            return False
        return self.matrix[y][x]
