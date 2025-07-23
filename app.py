
import os
import re
import streamlit as st
from transformers import pipeline
from PyPDF2 import PdfReader
from docx import Document
from pyngrok import ngrok

SUMMARIZATION_MODELS = {
    "BART Large CNN": "facebook/bart-large-cnn",
    "T5 Small": "t5-small",
    "DistilBART CNN": "sshleifer/distilbart-cnn-12-6",
}

@st.cache_resource
def initialize_summarizer(model_name: str):
    st.write(f"Loading {model_name} model...")
    try:
        summarizer = pipeline("summarization", model=model_name)
        st.success(f"{model_name} model loaded!")
        return summarizer
    except Exception as e:
        st.error(f"Error initializing summarizer model '{model_name}': {str(e)}")
        return None

def clean_text(text):
    return re.sub(r'\s+', ' ', text.strip())

def remove_duplicates(summary):
    sentences = summary.split('. ')
    unique_sentences = []
    for s in sentences:
        if s and s not in unique_sentences:
            unique_sentences.append(s)
    return '. '.join(unique_sentences) + ('.' if summary.endswith('.') else '')

def chunk_text(text, max_words=1024):
    words = text.split()
    for i in range(0, len(words), max_words):
        yield ' '.join(words[i:i+max_words])

def summarize_text(text, model_name, max_length=200, min_length=100):
    summarizer = initialize_summarizer(model_name)
    if not summarizer:
        return "Error: Summarizer not initialized."
    text = clean_text(text)
    if not text:
        return "Error: Input text is empty."
    try:
        if len(text.split()) <= 1024:
            summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False, num_beams=4)
            return remove_duplicates(summary[0]['summary_text'])
        else:
            chunks = list(chunk_text(text))
            summaries = []
            for chunk in chunks:
                summary = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False, num_beams=4)
                summaries.append(summary[0]['summary_text'])
            combined_summary = ' '.join(summaries)
            return remove_duplicates(combined_summary)
    except Exception as e:
        return f"Error during summarization: {str(e)}"

def summarize_file(uploaded_file, model_name, max_length=200, min_length=100):
    try:
        if uploaded_file.name.endswith('.pdf'):
            pdf_reader = PdfReader(uploaded_file)
            text = "".join(page.extract_text() or "" for page in pdf_reader.pages)
        elif uploaded_file.name.endswith('.docx'):
            doc = Document(uploaded_file)
            text = " ".join(paragraph.text for paragraph in doc.paragraphs)
        else:
            text = uploaded_file.read().decode('utf-8')
        return summarize_text(text, model_name, max_length, min_length)
    except Exception as e:
        return f"Error processing file: {str(e)}"

def main():
    st.title("QuickSum AI")
    st.markdown("Enter text or upload files to generate summaries using various pre-trained models.")

    st.sidebar.header("Summarization Model Options")
    selected_model_display_name = st.sidebar.selectbox(
        "Choose a summarization model:",
        list(SUMMARIZATION_MODELS.keys()),
        index=0
    )
    selected_model_id = SUMMARIZATION_MODELS[selected_model_display_name]

    tab1, tab2 = st.tabs(["Manual Input", "File Upload"])

    with tab1:
        st.subheader("Manual Text Input")
        text_input = st.text_area("Input Text", placeholder="Enter or paste your text here...", height=200)
        max_length = st.slider("Maximum Summary Length", 50, 300, 200)
        min_length = st.slider("Minimum Summary Length", 10, 150, 100)

        if st.button("Summarize"):
            if text_input:
                with st.spinner("Generating summary..."):
                    summary = summarize_text(text_input, selected_model_id, max_length, min_length)
                    st.subheader("Summary")
                    st.write(summary)
                    if summary and not summary.startswith("Error"):
                        st.download_button("Download Summary", summary, file_name="summary.txt")
            else:
                st.error("Please enter some text to summarize.")

    with tab2:
        st.subheader("File Upload")
        uploaded_files = st.file_uploader("Upload Text Files", type=["txt", "pdf", "docx"], accept_multiple_files=True)
        max_length_file = st.slider("Maximum Summary Length (Files)", 50, 300, 200, key="file_max_length")
        min_length_file = st.slider("Minimum Summary Length (Files)", 10, 150, 100, key="file_min_length")

        if uploaded_files and st.button("Summarize All Uploaded Files"):
            with st.spinner("Processing files and generating summaries..."):
                for uploaded_file in uploaded_files:
                    summary = summarize_file(uploaded_file, selected_model_id, max_length_file, min_length_file)
                    if summary and not summary.startswith("Error") and summary.strip().lower() != "null":
                        st.subheader(f"Summary for {uploaded_file.name}")
                        st.write(summary)
                        st.download_button(f"Download {uploaded_file.name}_summary", summary, file_name=f"{uploaded_file.name}_summary.txt")
                    elif summary.startswith("Error"):
                        st.error(f"Error for {uploaded_file.name}: {summary}")
                    else:
                        st.warning(f"No summary generated for {uploaded_file.name}. It might be empty or unreadable.")

if __name__ == "__main__":
    main()


