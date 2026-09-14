from fastapi import FastAPI, UploadFile, File

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "PDF Agent API is running"
    }


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    return {
        "filename": file.filename,
        "message": "PDF uploaded successfully"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )