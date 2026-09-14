import streamlit as st
import os

from app import load_pdf, split_documents


st.title("📄 PDF AI Agent")

st.write("Upload a single PDF and explore its content.")

uploaded_file = st.file_uploader(
    "Upload a PDF file",
    type=["pdf"]
)


if uploaded_file is not None:

    os.makedirs("pdfs", exist_ok=True)

    pdf_path = os.path.join(
        "pdfs",
        uploaded_file.name
    )

    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("PDF uploaded successfully!")

    if st.button("Process PDF"):

        with st.spinner("Reading PDF..."):

            documents = load_pdf(pdf_path)
            chunks = split_documents(documents)

        st.success("PDF processed successfully!")

        st.write(f"📄 Pages: {len(documents)}")
        st.write(f"🧩 Text chunks: {len(chunks)}")

        st.subheader("PDF Content")

        for i, chunk in enumerate(chunks[:5]):

            st.write(f"### Chunk {i + 1}")

            st.write(chunk.page_content)