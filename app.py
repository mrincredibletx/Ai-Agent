from fastapi import FastAPI, UploadFile, File
from pypdf import PdfReader
import tempfile
import os

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "PDF Agent API is running"
    }


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    # Check PDF
    if not file.filename.lower().endswith(".pdf"):
        return {
            "error": "Only PDF files are allowed"
        }

    # Read uploaded file
    contents = await file.read()

    # Create temporary PDF
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        temp_file.write(contents)
        temp_path = temp_file.name

    try:

        # Read PDF
        reader = PdfReader(temp_path)

        text = ""

        # Extract text from every page
        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return {
            "filename": file.filename,
            "pages": len(reader.pages),
            "text": text
        }

    finally:

        # Delete temporary file
        os.remove(temp_path)


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )