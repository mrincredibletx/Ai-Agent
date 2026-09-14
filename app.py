from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from pypdf import PdfReader
from langchain_openai import ChatOpenAI
import os
import tempfile


# =========================
# API KEY
# =========================

os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"


# =========================
# AI MODEL
# =========================

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)


# =========================
# FASTAPI
# =========================

app = FastAPI()


# =========================
# PDF AGENT
# =========================

def analyze_pdf(text):

    prompt = f"""
You are a PDF analysis agent.

Analyze the PDF given below.

Tell the user:

1. What this PDF is about
2. Short summary
3. Main topics
4. Important points
5. Important facts, dates and numbers
6. Conclusion

Explain everything in simple language.

PDF CONTENT:

{text}
"""

    response = llm.invoke(prompt)

    return response.content


# =========================
# FRONTEND
# =========================

HTML = """
<!DOCTYPE html>

<html>

<head>

<title>PDF Agent</title>

<style>

body {
    font-family: Arial;
    background: #111827;
    color: white;
    max-width: 900px;
    margin: auto;
    padding: 40px;
}

.box {
    background: #1f2937;
    padding: 30px;
    border-radius: 15px;
}

button {
    padding: 12px 25px;
    margin-top: 15px;
    cursor: pointer;
}

#result {
    margin-top: 30px;
    background: #1f2937;
    padding: 25px;
    border-radius: 15px;
    white-space: pre-wrap;
}

</style>

</head>

<body>

<h1>📄 PDF AI Agent</h1>

<div class="box">

<h2>Upload PDF</h2>

<input
    type="file"
    id="pdf"
    accept=".pdf"
>

<br>

<button onclick="analyzePDF()">
    Analyze PDF
</button>

</div>

<div id="result">
Upload a PDF to start...
</div>


<script>

async function analyzePDF() {

    const input = document.getElementById("pdf");
    const result = document.getElementById("result");

    if (!input.files.length) {

        result.innerText = "Please select a PDF.";

        return;
    }

    const formData = new FormData();

    formData.append("file", input.files[0]);

    result.innerText = "🤖 Reading PDF...";

    try {

        const response = await fetch(
            "/analyze",
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (data.error) {

            result.innerText = "❌ " + data.error;

            return;
        }

        result.innerText = data.analysis;

    } catch (error) {

        result.innerText =
            "❌ Error: " + error.message;

    }

}

</script>

</body>

</html>
"""


# =========================
# HOME PAGE
# =========================

@app.get("/", response_class=HTMLResponse)
async def home():

    return HTML


# =========================
# PDF UPLOAD
# =========================

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    # Only PDF
    if not file.filename.lower().endswith(".pdf"):

        return {
            "error": "Only PDF files are allowed."
        }

    # Read uploaded file
    contents = await file.read()

    # Create temporary PDF
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp:

        temp.write(contents)

        temp_path = temp.name


    try:

        # Read PDF
        reader = PdfReader(temp_path)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:

                text += page_text + "\n"


        if not text.strip():

            return {
                "error": "Could not extract text from this PDF."
            }


        # Send to AI agent
        result = analyze_pdf(text)


        return {
            "filename": file.filename,
            "analysis": result
        }


    finally:

        os.remove(temp_path)


# =========================
# START SERVER
# =========================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )