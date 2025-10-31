# QR Code Generator API

A simple FastAPI application that generates QR codes for URLs with optional custom logos and automatically uploads them to AWS S3 storage.

## Description

This project provides a REST API for generating customized QR codes. You can create QR codes for any URL and optionally add a logo in the center. The generated QR codes are automatically uploaded to AWS S3 and you receive a presigned URL to access the image.

## Features

-   **QR Code Generation**: Create QR codes for any URL
-   **Logo Integration**: Add custom logos to the center of QR codes
-   **Cloud Storage**: Automatic upload to AWS S3
-   **Transparent Background**: QR codes with transparent backgrounds
-   **High Error Correction**: Ensures QR codes work even if partially damaged
-   **REST API**: Simple HTTP endpoints for easy integration
-   **Auto-generated Documentation**: Interactive API docs with Swagger UI

## Installation

1. **Clone the repository**:

    ```bash
    git clone <repository-url>
    cd qrcode-generator
    ```

2. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Configure AWS credentials**:

    Create a `.env` file using the `.env.example` template and add your AWS credentials.

## How to Run

Start the FastAPI development server:

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## Access Links

Once the application is running, you can access:

-   **API Base URL**: `http://localhost:8000`
-   **Interactive API Documentation (Swagger UI)**: `http://localhost:8000/docs`
-   **Alternative API Documentation (ReDoc)**: `http://localhost:8000/redoc`


## Requirements

-   Python 3.8+
-   AWS S3 bucket
-   AWS credentials with S3 upload permissions

## Dependencies

-   **FastAPI**: Web framework for building APIs
-   **Pillow**: Image processing
-   **qrcode**: QR code generation
-   **boto3**: AWS S3 integration
-   **uvicorn**: ASGI server
