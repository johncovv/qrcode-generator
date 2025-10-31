from fastapi import UploadFile, APIRouter
from typing import Optional

from core import QrCodeData

router = APIRouter(prefix="/qr-code", tags=["QR Code Generation"])


@router.post("/generate", response_model=QrCodeData)
async def generate_qr(
    url: str,
    file: Optional[UploadFile] = None,
    border: int = 2,
):
    from core import qrcode_generator

    image_bytes = await file.read() if file else None

    qr_code_data = qrcode_generator.generate(
        url,
        image_bytes=image_bytes,
        qr_border=border,
    )

    return qr_code_data
