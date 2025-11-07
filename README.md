# PDF RAG QA Bot

A Streamlit application that allows users to upload PDF documents and ask questions about them using Llama-3.3-70B model via Groq API.

## Features

- 📄 Upload and process PDF documents
- 🤖 Ask questions about the document content using AI
- 📊 View source chunks used to generate answers
- ✨ Smart relevance detection - only answers when information is available in the document

## Tech Stack

- **Streamlit** - Web framework
- **LangChain** - LLM framework
- **ChromaDB** - Vector database for document embeddings
- **Groq API** - LLM inference (Llama-3.3-70B)
- **HuggingFace** - Embedding models

## Setup

### Local Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

### Streamlit Cloud Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## Usage

1. Upload a PDF file
2. Wait for the document to be processed
3. Ask questions about the document content
4. View answers with source citations

## Requirements

- Python 3.8+
- Groq API key

