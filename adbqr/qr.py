import qrcode

class QrRenderer:
    def __init__(self, data: str):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=1,
            border=2,  # Minimal internal border, we will add massive manual padding
        )
        qr.add_data(data)
        qr.make(fit=True)
        self.matrix = qr.modules
        self.width = len(self.matrix[0])
        self.height = len(self.matrix)

    def render(self):
        # Force Black Foreground (30) and White Background (47)
        COLOR = "\x1b[30;47m"
        RESET = "\x1b[0m"

        # 6 spaces of pure white padding on left and right
        pad_x = "      "
        blank_line = COLOR + pad_x + (" " * self.width) + pad_x + RESET

        print()
        # Top quiet zone
        print(blank_line)
        print(blank_line)

        for y in range(0, self.height, 2):
            row_str = COLOR + pad_x
            for x in range(self.width):
                top = self.matrix[y][x]
                bottom = self.matrix[y+1][x] if (y+1) < self.height else False

                # Use half-blocks to ensure perfect square aspect ratio
                if top and bottom:
                    row_str += '█'
                elif top and not bottom:
                    row_str += '▀'
                elif not top and bottom:
                    row_str += '▄'
                else:
                    row_str += ' '
            row_str += pad_x + RESET
            print(row_str)

        # Bottom quiet zone
        print(blank_line)
        print(blank_line)
        print()
