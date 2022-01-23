from __future__ import annotations
import qrcode
from PIL import Image
from helpers.colors import Color, Colors
from dataclasses import dataclass


@dataclass
class QRCode:
    data: str
    logo_path: str | None = None
    output_name: str = "QR.png"
    quality: int = 40
    front_color: Color = Colors.black
    back_color: Color = Colors.white
    border: int = 2

    def generate(self):
        self.basewidth = self.quality * 9
        # generate
        QRcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=self.quality, border=self.border)

        # adding URL or text to QRcode
        QRcode.add_data(self.data)

        # generating QR code
        QRcode.make()

        # adding color to QR code
        QRimg = QRcode.make_image(fill_color=self.front_color.color, back_color=self.back_color.color).convert('RGB')

        # set size of QR code
        if self.logo_path is not None:
            logo = Image.open(self.logo_path)
            new_image = Image.new("RGBA", logo.size, (*self.back_color.color, 255))  # Create a white rgba background
            new_image.paste(logo, (0, 0), logo)              # Paste the image on the background. Go to the links given below for details.
            new_image.convert('RGB')
            logo = new_image
            # adjust image size
            wpercent = (self.basewidth/float(logo.size[0]))
            hsize = int((float(logo.size[1])*float(wpercent)))
            logo = logo.resize((self.basewidth, hsize), Image.ANTIALIAS)
            pos = ((QRimg.size[0] - logo.size[0]) // 2,
                   (QRimg.size[1] - logo.size[1]) // 2)
            QRimg.paste(logo, pos)

        # save the QR code generated
        QRimg.save(self.output_name)

        print('QR code generated!')


if __name__ == "__main__":
    code = QRCode("P9jkUcIwlGVEp9nygG64", logo_path="Logo.png")
    code.generate()
