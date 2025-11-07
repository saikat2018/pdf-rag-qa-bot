import os
from dotenv import load_dotenv

from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
# Try to import RetrievalQA with multiple fallback options
RETRIEVAL_QA_AVAILABLE = False
RetrievalQA = None
create_retrieval_chain = None
create_stuff_documents_chain = None
ChatPromptTemplate = None

try:
    from langchain.chains import RetrievalQA
    RETRIEVAL_QA_AVAILABLE = True
except ImportError:
    try:
        from langchain.chains.retrieval_qa.base import RetrievalQA
        RETRIEVAL_QA_AVAILABLE = True
    except ImportError:
        # Use modern LangChain API as fallback
        try:
            from langchain.chains import create_retrieval_chain
            from langchain.chains.combine_documents import create_stuff_documents_chain
            from langchain_core.prompts import ChatPromptTemplate
            RETRIEVAL_QA_AVAILABLE = False
        except ImportError:
            raise ImportError("Could not import RetrievalQA or modern LangChain retrieval chain. Please check your LangChain version.")


# Load environment variables from .env file
load_dotenv()

working_dir = os.path.dirname(os.path.abspath((__file__)))

# Lazy initialization of embedding model to avoid import errors at module load time
_embedding = None

def get_embedding():
    """Get or create the embedding model instance."""
    global _embedding
    if _embedding is None:
        try:
            _embedding = HuggingFaceEmbeddings()
        except ImportError as e:
            raise ImportError(
                "Could not import sentence-transformers. Please install it with: pip install sentence-transformers"
            ) from e
    return _embedding

# Lazy initialization of LLM to avoid errors at module load time
_llm = None

def get_llm():
    """Get or create the LLM instance."""
    global _llm
    if _llm is None:
        _llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0
        )
    return _llm


def process_document_to_chroma_db(file_name):
    # Load the PDF document using UnstructuredPDFLoader
    loader = UnstructuredPDFLoader(f"{working_dir}/{file_name}")
    documents = loader.load()
    # Split the text into chunks for embedding
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200
    )
    texts = text_splitter.split_documents(documents)
    # Store the document chunks in a Chroma vector database
    embedding = get_embedding()
    vectordb = Chroma.from_documents(
        documents=texts,
        embedding=embedding,
        persist_directory=f"{working_dir}/doc_vectorstore"
    )
    return 0


def answer_question(user_question):
    """
    Answer a question based on the uploaded document.
    Returns a dictionary with 'answer' and 'sources' keys.
    If the question is not relevant, sources will be None.
    """
    # Load the persistent Chroma vector database
    embedding = get_embedding()
    vectordb = Chroma(
        persist_directory=f"{working_dir}/doc_vectorstore",
        embedding_function=embedding
    )
    
    # Create a retriever for document search
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    
    # Retrieve documents for source display
    source_documents = retriever.get_relevant_documents(user_question)
    
    not_found_message = "I could not find relevant information to answer your question in the uploaded document. Please make sure your question is related to the content of the PDF you uploaded."
    
    # Check if documents were retrieved
    if not source_documents:
        return {"answer": not_found_message, "sources": None}
    
    # Note: We're not doing a strict similarity threshold check here
    # Instead, we'll let the LLM decide if the retrieved context is relevant
    # This prevents false negatives where relevant queries are incorrectly blocked

    llm = get_llm()
    
    if RETRIEVAL_QA_AVAILABLE:
        # Use traditional RetrievalQA chain with updated prompt
        from langchain.prompts import PromptTemplate
        
        prompt_template = """You are a helpful assistant. Answer the question based ONLY on the provided context from the document.

IMPORTANT: 
- If the context contains relevant information to answer the question, provide a clear and helpful answer.
- Only if the context is completely irrelevant or does not contain ANY information related to the question, respond with: "I could not find relevant information to answer your question in the uploaded document. Please make sure your question is related to the content of the PDF you uploaded."
- Be thorough and use the context to provide the best answer you can.

Context: {context}

Question: {question}

Answer:"""
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True
        )
        response = qa_chain.invoke({"query": user_question})
        answer = response["result"]
        
        # Get source documents from response
        if "source_documents" in response:
            source_documents = response["source_documents"]
        
        # Check if the LLM explicitly indicates it cannot answer
        # Only return "not found" if the answer matches our exact message or clearly states no information
        answer_lower = answer.lower().strip()
        # Check if answer is exactly our not found message or very similar
        if (answer_lower == not_found_message.lower() or 
            (len(answer_lower) < 100 and 
             "could not find" in answer_lower and 
             "uploaded document" in answer_lower)):
            return {"answer": not_found_message, "sources": None}
    else:
        # Use modern LangChain retrieval chain with updated prompt
        prompt = ChatPromptTemplate.from_template("""You are a helpful assistant. Answer the question based ONLY on the provided context from the document.

IMPORTANT: 
- If the context contains relevant information to answer the question, provide a clear and helpful answer based on that context.
- Only if the context is completely irrelevant or does not contain ANY information related to the question, respond with: "I could not find relevant information to answer your question in the uploaded document. Please make sure your question is related to the content of the PDF you uploaded."
- Be thorough and use the context to provide the best answer you can.
- Do not make up information, but do your best to answer from the context provided.

Context: {context}

Question: {input}

Answer:""")

        # Create a document chain
        document_chain = create_stuff_documents_chain(llm, prompt)
        
        # Create a retrieval chain
        qa_chain = create_retrieval_chain(retriever, document_chain)
        
        # Invoke the chain
        response = qa_chain.invoke({"input": user_question})
        answer = response["answer"]
        
        # Get source documents from response (modern API includes them in 'context')
        # The retrieval chain returns documents in the 'context' key
        # We use the documents we retrieved earlier for consistency
        # (The retrieval chain uses the same retriever, so they should be the same documents)
        
        # Check if the LLM explicitly indicates it cannot answer
        # Only return "not found" if the answer matches our exact message or clearly states no information
        answer_lower = answer.lower().strip()
        # Check if answer is exactly our not found message or very similar
        if (answer_lower == not_found_message.lower() or 
            (len(answer_lower) < 100 and 
             "could not find" in answer_lower and 
             "uploaded document" in answer_lower)):
            return {"answer": not_found_message, "sources": None}

    # Format sources for display
    formatted_sources = []
    for i, doc in enumerate(source_documents, 1):
        source_text = doc.page_content.strip()
        # Truncate long sources for display
        if len(source_text) > 500:
            source_text = source_text[:500] + "..."
        formatted_sources.append({
            "chunk": i,
            "content": source_text,
            "metadata": doc.metadata if hasattr(doc, 'metadata') else {}
        })
    
    return {"answer": answer, "sources": formatted_sources}
