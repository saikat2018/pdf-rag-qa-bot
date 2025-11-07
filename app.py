import os

import streamlit as st

from rag_utility import process_document_to_chroma_db, answer_question


# set the working directory
working_dir = os.path.dirname(os.path.abspath((__file__)))

# Initialize session state
if 'answer_result' not in st.session_state:
    st.session_state.answer_result = None
if 'document_processed' not in st.session_state:
    st.session_state.document_processed = False

st.title("🦙 Llama-3.3-70B - Document RAG")

# file uploader widget
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Check if this is a new file upload (not just a re-run)
    if not st.session_state.document_processed or uploaded_file.name != st.session_state.get('uploaded_file_name', ''):
        # define save path
        save_path = os.path.join(working_dir, uploaded_file.name)
        #  save the file
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        process_document = process_document_to_chroma_db(uploaded_file.name)
        st.session_state.document_processed = True
        st.session_state.uploaded_file_name = uploaded_file.name
        st.session_state.answer_result = None  # Clear previous answer
        st.info("Document Processed Successfully")

# text widget to get user input
user_question = st.text_area("Ask your question about the document")

# Only process when the Answer button is clicked
if st.button("Answer"):
    if user_question.strip():
        # Only call answer_question when button is explicitly clicked
        with st.spinner("Processing your question..."):
            result = answer_question(user_question)
            st.session_state.answer_result = result
    else:
        st.session_state.answer_result = None
        st.warning("Please enter a question.")

# Display results from session state (only if they exist)
if st.session_state.answer_result is not None:
    result = st.session_state.answer_result
    
    # Extract answer and sources from result
    answer = result.get("answer", "")
    sources = result.get("sources", None)
    
    st.markdown("### Llama-3.3-70B Response")
    st.markdown(answer)
    
    # Display sources if available
    if sources:
        st.markdown("---")
        st.markdown("### 📄 Source Chunks")
        st.markdown("*The following document chunks were used to generate the answer:*")
        
        for source in sources:
            with st.expander(f"Source Chunk {source['chunk']}", expanded=False):
                st.markdown(source['content'])
                # Display metadata if available
                if source.get('metadata'):
                    metadata = source['metadata']
                    if metadata:
                        st.caption("**Metadata:**")
                        for key, value in metadata.items():
                            if key != 'source':  # Skip source path to keep it clean
                                st.caption(f"- {key}: {value}")
# Signature at the bottom
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Built by Saikat</p>", unsafe_allow_html=True)