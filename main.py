from fastapi import FastAPI, File, UploadFile


app = FastAPI(
    title="My QR Code Generator API",
)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the QR Code Generator API!"}


@app.post("/generate-qr")
async def generate_qr(url: str, image: UploadFile | None = File(None)):
    from core import qrcode_generator

    file_url = qrcode_generator.generate_qr_with_logo(url)

    return {"file_url": file_url}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
