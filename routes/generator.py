from fastapi import UploadFile, APIRouter
from typing import Optional

from core import QrCodeData, QrCodeGeneratorConfig

router = APIRouter(prefix="/qr-code", tags=["QR Code Generation"])


@router.post("/generate-and-upload", response_model=QrCodeData)
async def generate_qr(
    url: str,
    file: Optional[UploadFile] = None,
):
    from core import qrcode_generator

    image_bytes = await file.read() if file else None

    qr_code_data = qrcode_generator.generate_and_upload(
        url,
        image_bytes=image_bytes,
    )

    return qr_code_data


@router.get("/generate-on-memory")
async def generate_qr_on_memory(
    url: str,
    border: int = 2,
):
    from core import qrcode_generator
    from fastapi.responses import StreamingResponse

    qr_code_buffer = qrcode_generator.generate_on_memory(
        url, config=QrCodeGeneratorConfig(qr_border=border)
    )

    return StreamingResponse(qr_code_buffer, media_type="image/png")
