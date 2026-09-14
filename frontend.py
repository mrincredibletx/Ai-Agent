import os
import streamlit as st

from app import load_pdf, split_documents


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="DocuLens",
    page_icon="📑",
    layout="wide"
)


# -----------------------------
# Custom Styling
# -----------------------------
st.markdown("""
<style>
    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        opacity: 0.7;
        margin-bottom: 30px;
    }

    .upload-box {
        padding: 25px;
        border-radius: 15px;
        border: 1px solid rgba(128,128,128,0.3);
        margin-bottom: 20px;
    }

    .info-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.25);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------
# Session State
# -----------------------------
if "documents" not in st.session_state:
    st.session_state.documents = None

if "chunks" not in st.session_state:
    st.session_state.chunks = None

if "file_name" not in st.session_state:
    st.session_state.file_name = None


# -----------------------------
# Header
# -----------------------------
st.markdown(
    '<div class="main-title">📑 DocuLens</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Upload a document and explore its content intelligently.'
    '</div>',
    unsafe_allow_html=True
)


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.header("⚙️ Document Panel")

    st.write("Supported format")

    st.info("📄 PDF only")

    st.divider()

    st.caption(
        "DocuLens currently processes one PDF at a time."
    )


# -----------------------------
# Upload Section
# -----------------------------
st.markdown(
    '<div class="upload-box">',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Choose your PDF",
    type=["pdf"],
    accept_multiple_files=False
)

st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------
# Process Uploaded PDF
# -----------------------------
if uploaded_file:

    os.makedirs("pdfs", exist_ok=True)

    file_path = os.path.join(
        "pdfs",
        uploaded_file.name
    )

    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    st.session_state.file_name = uploaded_file.name

    st.success(
        f"Ready to process: {uploaded_file.name}"
    )

    process = st.button(
        "🔍 Analyze Document",
        use_container_width=True
    )

    if process:

        with st.spinner("Extracting document content..."):

            documents = load_pdf(file_path)
            chunks = split_documents(documents)

            st.session_state.documents = documents
            st.session_state.chunks = chunks

        st.success("Document analyzed successfully!")


# -----------------------------
# Results
# -----------------------------
if st.session_state.documents is not None:

    documents = st.session_state.documents
    chunks = st.session_state.chunks

    st.divider()

    st.subheader("📊 Document Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Pages",
            len(documents)
        )

    with col2:
        st.metric(
            "Text Sections",
            len(chunks)
        )

    with col3:
        st.metric(
            "Characters",
            sum(
                len(chunk.page_content)
                for chunk in chunks
            )
        )

    st.divider()

    # -------------------------
    # Content Viewer
    # -------------------------
    st.subheader("📖 Content Viewer")

    page_number = st.selectbox(
        "Select a page",
        range(1, len(documents) + 1)
    )

    selected_page = documents[page_number - 1]

    with st.expander(
        f"Page {page_number} content",
        expanded=True
    ):

        st.write(
            selected_page.page_content
        )

    # -------------------------
    # Chunk Explorer
    # -------------------------
    st.subheader("🧩 Text Chunk Explorer")

    chunk_number = st.number_input(
        "Choose chunk number",
        min_value=1,
        max_value=len(chunks),
        value=1
    )

    selected_chunk = chunks[chunk_number - 1]

    st.text_area(
        "Extracted text",
        selected_chunk.page_content,
        height=250
    )

    # -------------------------
    # File Information
    # -------------------------
    with st.expander("📌 File Information"):

        st.write(
            f"**File:** {st.session_state.file_name}"
        )

        st.write(
            f"**Pages:** {len(documents)}"
        )

        st.write(
            f"**Chunks:** {len(chunks)}"
        )

else:

    st.info(
        "👆 Upload a PDF above to start exploring the document."
    )