import streamlit as st
import tempfile
import os
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

# Step 2: Load Uploaded PDF
def load_document_from_upload(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    ext = os.path.splitext(uploaded_file.name)[1].lower()

    if ext == ".pdf":
        loader = PyMuPDFLoader(tmp_path)
    elif ext == ".txt":
        loader = TextLoader(tmp_path)
    else:
        st.error("Unsupported file format.")
        return []

    return loader.load()

# Step 3: Create ChromaDB Index
def create_chroma_index(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=80,
        separators=["\n\n", "\n", ".", " "]
    )
    chunks = splitter.split_documents(documents)

    embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = Chroma.from_documents(chunks, embedding=embedder, persist_directory="chroma_db")
    return vectordb

# === Streamlit UI ===
st.title("Smart Research Assistant")

uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

if uploaded_file is not None:
    st.success("File uploaded successfully!")

    # Step 2
    documents = load_document_from_upload(uploaded_file)
    st.write(f"Loaded {len(documents)} document chunks.")

    # Step 3
    vectordb = create_chroma_index(documents)
    st.success("ChromaDB index created!")

    # Load LLaMA 3 from Ollama
    llm = Ollama(model="llama3")    
    
    # Set up Retrieval-Augmented Generation (RAG) pipeline
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectordb.as_retriever(),
        return_source_documents=True
    )
 
    mode = st.radio("Choose Interaction Mode", ["Ask Anything", "Challenge Me"])

    if mode == "Ask Anything":
        st.subheader("Ask Anything About the Document")
        query = st.text_input("Enter your question:")
        if query:
            response = qa_chain(query)
            st.markdown("### Answer")
            st.write(response["result"])

            st.markdown("### Sources")
            for doc in response["source_documents"]:
                st.info(doc.page_content[:300] + "...")

    if mode == "Challenge Me":
        st.subheader("Challenge Me Mode")

        with st.spinner("Generating questions..."):
            context_text = "\n".join([doc.page_content for doc in documents[:3]])[:3000]
            prompt = f"""
            Based on the following document, generate 3 logic-based or comprehension-focused questions:
            {context_text}

            Format the output as:
            1. ...
            2. ...
            3. ...
            """
            questions_output = llm(prompt)

        questions = [q.strip()[3:] for q in questions_output.strip().split("\n") if q.strip().startswith(("1.", "2.", "3."))]

        user_answers = []
        if questions:
            st.success("Questions generated successfully!")

            for i, question in enumerate(questions):
                st.markdown(f"**Q{i+1}: {question}**")
                answer = st.text_input(f"Your Answer to Q{i+1}:", key=f"answer_{i}")
                user_answers.append((question, answer))

            if st.button("Submit Answers"):
                st.subheader("Evaluation Results")
                for i, (question, user_answer) in enumerate(user_answers):
                    eval_prompt = f"""
                    Question: {question}
                    User's Answer: {user_answer}

                    Evaluate the answer based on the document content. Be fair and objective.
                    Justify your evaluation with a reference to the source text.
                    """
                    response = qa_chain(eval_prompt)
                    result = response["result"]

                    st.markdown(f"**Q{i+1} Evaluation:**")
                    st.write(result)