from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_pdf(file_path):
    loader = PDFPlumberLoader(file_path)
    documents = loader.load()
    return documents


def split_documents(documents, chunk_size=1000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )

    return text_splitter.split_documents(documents)


if __name__ == "__main__":

    pdf_path = "sample.pdf"

    print("Loading PDF...")

    documents = load_pdf(pdf_path)

    print(f"PDF loaded successfully!")
    print(f"Total pages: {len(documents)}")

    chunks = split_documents(documents)

    print(f"Total chunks: {len(chunks)}")

    print("\nFirst chunk:")
    print(chunks[0].page_content)