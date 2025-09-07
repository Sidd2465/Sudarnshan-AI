import streamlit as st
from transformers import T5ForConditionalGeneration, T5Tokenizer
import pdfplumber
import textwrap

# Set up the Streamlit page
st.title("Sudarshan AI: Legal Document Simplifier & Q&A")
st.write("Upload your legal document (PDF) or paste text below to get a simplified summary and ask questions.")

@st.cache_resource
def load_summarization_model():
    model_name = "t5-small"
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_summarization_model()

def extract_text_from_pdf(pdf_file) -> str:
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
    return text

def chunk_text(text, max_tokens=450):
    # Rough chunking by characters (approximate tokens)
    chunks = textwrap.wrap(text, max_tokens*4)  # approx 4 chars per token
    return chunks

uploaded_file = st.sidebar.file_uploader("Upload a PDF legal document", type=["pdf"])

if "document_text" not in st.session_state:
    st.session_state.document_text = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if uploaded_file is not None:
    with st.spinner("Extracting text from PDF..."):
        extracted_text = extract_text_from_pdf(uploaded_file)
        if extracted_text:
            st.session_state.document_text = extracted_text
            st.success("PDF text extracted successfully!")

document_text = st.text_area(
    "Legal Document Text",
    value=st.session_state.document_text,
    height=300,
    placeholder="Paste your legal document here or upload a PDF..."
)

def summarize_text(text):
    chunks = chunk_text(text)
    summaries = []
    for chunk in chunks:
        input_text = "summarize: " + chunk
        inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
        summary_ids = model.generate(
            inputs,
            max_length=150,
            min_length=30,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True
        )
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        summaries.append(summary)
    combined_summary = " ".join(summaries)
    return combined_summary

if st.button("Simplify Document"):
    if document_text.strip():
        with st.spinner("Summarizing document..."):
            summary = summarize_text(document_text)
            st.session_state.summary = summary
            st.subheader("Simplified Summary")
            st.success(summary)
    else:
        st.warning("Please provide some text to summarize.")

st.markdown("---")
st.subheader("Ask Questions About Your Document")

def generate_answer(question: str, context: str) -> str:
    input_text = f"question: {question} context: {context}"
    inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(
        inputs,
        max_length=100,
        num_beams=4,
        early_stopping=True
    )
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer

user_question = st.text_input("Enter your question here:")

if st.button("Get Answer"):
    if user_question.strip() and (st.session_state.summary or document_text.strip()):
        context = st.session_state.summary if st.session_state.summary else document_text
        with st.spinner("Generating answer..."):
            answer = generate_answer(user_question, context)
            st.session_state.chat_history.append({"question": user_question, "answer": answer})
    else:
        st.warning("Please upload or paste a document and enter a question.")

if st.session_state.chat_history:
    for chat in st.session_state.chat_history:
        st.markdown(f"**Q:** {chat['question']}")
        st.markdown(f"**A:** {chat['answer']}")
        st.markdown("---")

if st.sidebar.button("Clear All"):
    st.session_state.document_text = ""
    st.session_state.summary = ""
    st.session_state.chat_history = []
    st.experimental_rerun()

st.sidebar.markdown("""
### How it Works
- Upload a PDF or paste your legal document text.
- The app extracts text from PDFs and summarizes it using the **T5-small** model.
- You can ask questions about the document in the chatbot section.
- Answers are generated based on the document content using the same model for demonstration.
""")
