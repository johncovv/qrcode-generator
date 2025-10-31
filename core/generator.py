from io import BufferedReader
from PIL import Image, ImageDraw
from uuid import uuid4
from qrcode.constants import ERROR_CORRECT_H
from qrcode.image.pil import PilImage
from typing import TypedDict, Optional
from qrcode import QRCode
from pydantic import BaseModel


from core import storage


class QrCodeData(TypedDict):
    file_url: str
    file_name: str


class QrCodeGeneratorConfig(BaseModel):
    qr_border: int = 2
    hole_ratio: float = 0.2


class QrCodeGenerator:
    def generate_on_memory(
        self,
        url: str,
        image_bytes: bytes | None = None,
        config: Optional[QrCodeGeneratorConfig] = None,
    ) -> BufferedReader:
        temp_path, _ = self._generate(url, image_bytes=image_bytes, config=config)

        return open(temp_path, "rb")

    def generate_and_upload(
        self,
        url: str,
        image_bytes: bytes | None = None,
        config: Optional[QrCodeGeneratorConfig] = None,
    ) -> QrCodeData:
        temp_path, filename = self._generate(
            url, image_bytes=image_bytes, config=config
        )

        # Upload the file to S3 and get a temporary URL
        file_url = self._upload_file(temp_path, filename)
        return QrCodeData(file_url=file_url, file_name=filename)

    def _generate(
        self,
        url: str,
        image_bytes: bytes | None = None,
        config: Optional[QrCodeGeneratorConfig] = None,
    ) -> tuple[str, str]:
        qr = QRCode(
            version=1,
            error_correction=ERROR_CORRECT_H,
            border=config.qr_border if config else 2,
            box_size=10,
        )

        qr.add_data(url)
        qr.make(fit=True)

        qr_img = qr.make_image(
            fill_color="black", back_color="transparent", image_factory=PilImage
        ).convert("RGBA")

        url_name = url.split("//")[-1].split("/")[0]
        filename = f"{url_name}_{uuid4().hex}.png"

        # if provided, attach image at the center of the QR code
        if image_bytes:
            qr_img = self._attach_image_on_qr(
                qr_img, image_bytes, hole_ratio=config.hole_ratio if config else 0.2
            )

        # Save QR code to a temporary file
        temp_path = f"/tmp/{filename}"
        qr_img.save(temp_path, format="PNG", optimize=True)

        return temp_path, filename

    def _attach_image_on_qr(
        self, qr_image: Image.Image, image_bytes: bytes, hole_ratio: float = 0.2
    ) -> Image.Image:
        import io

        qr_width, qr_height = qr_image.size
        hole_size = int(qr_width * hole_ratio)

        x = (qr_width - hole_size) // 2
        y = (qr_height - hole_size) // 2

        # Create a "hole" in the center of the QR code
        mask = qr_image.getchannel("A")
        draw = ImageDraw.Draw(mask)
        draw.rectangle([(x, y), (x + hole_size, y + hole_size)], fill=0)
        qr_image.putalpha(mask)

        image = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
        image = image.resize((hole_size, hole_size), Image.Resampling.LANCZOS)
        qr_image.alpha_composite(image, (x, y))

        return qr_image

    def _upload_file(self, file_path: str, filename: str) -> str:
        return storage.upload_file(file_path, filename)


qrcode_generator = QrCodeGenerator()
