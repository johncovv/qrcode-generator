from PIL import Image, ImageDraw
from uuid import uuid4
from qrcode.constants import ERROR_CORRECT_H
from qrcode.image.pil import PilImage
from qrcode import QRCode

from core import storage


class QrCodeGenerator:

    def generate_qr_with_logo(self, url: str, image_path: str | None = None) -> str:
        qr = QRCode(
            version=1,
            error_correction=ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )

        qr.add_data(url)
        qr.make(fit=True)
        qr_img = qr.make_image(
            fill_color="black", back_color="transparent", image_factory=PilImage
        ).convert(
            "RGBA",
        )

        url_name = url.split("//")[-1].split("/")[0]
        filename = f"{url_name}_{uuid4().hex}.png"

        if image_path:
            image = Image.open(image_path)
            qr_width, qr_height = qr_img.size
            logo_size = int(qr_width * 0.2)
            image = image.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            x = (qr_width - logo_size) // 2
            y = (qr_height - logo_size) // 2

            draw = ImageDraw.Draw(qr_img)
            padding = int(logo_size * 0.05)  # borda extra branca em volta
            draw.rectangle(
                [
                    (x - padding, y - padding),
                    (x + logo_size + padding, y + logo_size + padding),
                ],
            )
            qr_img.paste(image, (x, y), mask=image if image.mode == "RGBA" else None)

        temp_path = f"/tmp/{filename}"
        qr_img.save(temp_path)

        file_url = storage.upload_file(temp_path, filename)
        return file_url


qrcode_generator = QrCodeGenerator()
